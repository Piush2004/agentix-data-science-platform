import logging
import os
from contextvars import ContextVar
from fastapi import HTTPException
from core.context import current_user_id

logger = logging.getLogger(__name__)

class TenantManager:
    """
    Centralizes all multi-tenant logic, enforcing strict physical and logical boundaries
    between user resources (Datasets, Jobs, Memory).
    """
    
    @staticmethod
    def get_current_tenant() -> str:
        """Retrieves the active tenant UUID for the current execution context."""
        try:
            return current_user_id.get()
        except LookupError:
            raise HTTPException(status_code=401, detail="Unauthorized: No active tenant context found.")
            
    @staticmethod
    def validate_tenant_access(resource_owner_id: str):
        """
        Hard enforcement. Throws 403 if the requesting tenant does not match the resource owner.
        """
        active_tenant = TenantManager.get_current_tenant()
        if active_tenant != resource_owner_id:
            logger.critical(f"Security Violation! Tenant {active_tenant} attempted to access resource owned by {resource_owner_id}.")
            raise HTTPException(status_code=403, detail="Forbidden: Resource belongs to a different tenant.")
            
    @staticmethod
    def setup_tenant_workspace(tenant_id: str, base_dir: str):
        """
        Provisions a physically isolated directory structure for a newly active tenant.
        """
        tenant_path = os.path.join(base_dir, tenant_id)
        models_path = os.path.join(tenant_path, "models")
        
        os.makedirs(tenant_path, exist_ok=True)
        os.makedirs(models_path, exist_ok=True)
        return tenant_path

tenant_manager = TenantManager()
