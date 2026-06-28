from django.contrib import admin
from .models import IdeaTimestamp, BlockchainCertificate


@admin.register(IdeaTimestamp)
class IdeaTimestampAdmin(admin.ModelAdmin):
    list_display = ["block_number", "idea", "idea_hash", "timestamp"]
    readonly_fields = ["idea_hash", "previous_hash", "block_number", "timestamp"]


@admin.register(BlockchainCertificate)
class BlockchainCertificateAdmin(admin.ModelAdmin):
    list_display = ["certificate_id", "idea_name", "owner_name", "issued_at", "is_valid"]
    list_filter = ["is_valid"]
