import { motion } from 'framer-motion';
import { Building2, Users, FileCheck, ShieldCheck } from 'lucide-react';

export const EnterpriseFeatures = () => {
  return (
    <section className="py-24 bg-zinc-950 relative" id="enterprise">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center gap-16">
          <div className="flex-1">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-3xl md:text-5xl font-semibold tracking-tight mb-6"
            >
              Enterprise-ready out of the box.
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-lg text-muted-foreground mb-8"
            >
              Designed for the strict compliance and security requirements of Fortune 500 companies. Kortex provides granular control over your data, access, and AI models.
            </motion.p>

            <div className="space-y-6">
              {[
                { icon: <ShieldCheck />, title: "SSO & SAML Integration", desc: "Integrate seamlessly with Okta, Azure AD, and Ping Identity." },
                { icon: <Users />, title: "Granular RBAC", desc: "Define precise access policies at the document or section level." },
                { icon: <FileCheck />, title: "Audit Logging", desc: "Comprehensive logs for compliance, security reviews, and usage tracking." },
                { icon: <Building2 />, title: "VPC Deployment", desc: "Deploy Kortex securely within your own virtual private cloud." }
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  className="flex gap-4"
                >
                  <div className="mt-1 text-purple-400">{item.icon}</div>
                  <div>
                    <h4 className="font-semibold text-lg">{item.title}</h4>
                    <p className="text-muted-foreground">{item.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="flex-1 w-full">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/20 to-blue-500/20 blur-3xl -z-10" />
              <div className="glass-card rounded-2xl border border-white/10 p-8 shadow-2xl relative overflow-hidden bg-background/50 backdrop-blur-xl">
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/5">
                    <div>
                      <div className="font-medium text-sm">Finance Department Access</div>
                      <div className="text-xs text-green-400">Policy Active</div>
                    </div>
                    <div className="w-10 h-6 bg-green-500/20 rounded-full border border-green-500/50 flex items-center justify-end p-1">
                      <div className="w-4 h-4 bg-green-400 rounded-full" />
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/5">
                    <div>
                      <div className="font-medium text-sm">Engineering Vault (Restricted)</div>
                      <div className="text-xs text-yellow-400">Strict Auth Required</div>
                    </div>
                    <div className="w-10 h-6 bg-white/10 rounded-full border border-white/20 flex items-center p-1">
                      <div className="w-4 h-4 bg-white/40 rounded-full" />
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/5">
                    <div>
                      <div className="font-medium text-sm">External Contractors</div>
                      <div className="text-xs text-red-400">Access Revoked</div>
                    </div>
                    <div className="w-10 h-6 bg-red-500/20 rounded-full border border-red-500/50 flex items-center justify-start p-1">
                      <div className="w-4 h-4 bg-red-400 rounded-full" />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
};
