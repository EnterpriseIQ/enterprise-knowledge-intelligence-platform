from src.security.rbac import RBACEngine

rbac = RBACEngine()

# Suppose the user "fin_carol" belongs to Finance.
# Let's see what happens if they request "Admin" role.
print("Requested as Admin by fin_carol:", rbac.resolve_role(user_id="fin_carol", role="Admin"))
print("Requested without role by fin_carol:", rbac.resolve_role(user_id="fin_carol", role=None))
