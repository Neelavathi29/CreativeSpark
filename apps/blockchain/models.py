import hashlib
import json
from datetime import datetime
from django.db import models
from django.conf import settings


def generate_idea_hash(idea_data):
    data_str = json.dumps(idea_data, sort_keys=True, default=str)
    return hashlib.sha256(data_str.encode()).hexdigest()


class IdeaTimestamp(models.Model):
    idea = models.OneToOneField("ideas.StartupIdea", on_delete=models.CASCADE, related_name="blockchain_timestamp")
    idea_hash = models.CharField(max_length=64, unique=True, editable=False)
    previous_hash = models.CharField(max_length=64, blank=True, null=True)
    block_number = models.PositiveIntegerField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-block_number"]

    def __str__(self):
        return f"Block #{self.block_number} - {self.idea.startup_name}"

    def save(self, *args, **kwargs):
        if not self.idea_hash:
            idea_data = {
                "id": self.idea.id,
                "name": self.idea.startup_name,
                "founder": self.idea.founder_name,
                "problem": self.idea.problem_statement,
                "solution": self.idea.proposed_solution,
                "industry": self.idea.industry,
                "user_id": self.idea.user_id,
            }
            self.idea_hash = generate_idea_hash(idea_data)
        if not self.block_number:
            last_block = IdeaTimestamp.objects.order_by("-block_number").first()
            self.previous_hash = last_block.idea_hash if last_block else "0" * 64
            self.block_number = (last_block.block_number + 1) if last_block else 1
        super().save(*args, **kwargs)


class BlockchainCertificate(models.Model):
    idea_timestamp = models.OneToOneField(IdeaTimestamp, on_delete=models.CASCADE, related_name="certificate")
    certificate_id = models.CharField(max_length=64, unique=True, editable=False)
    owner_name = models.CharField(max_length=200)
    idea_name = models.CharField(max_length=200)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Certificate {self.certificate_id[:16]}... - {self.idea_name}"

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            raw = f"{self.idea_timestamp.idea_hash}{self.owner_name}{datetime.now().isoformat()}"
            self.certificate_id = hashlib.sha256(raw.encode()).hexdigest()
        super().save(*args, **kwargs)
