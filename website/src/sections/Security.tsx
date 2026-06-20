import { motion } from 'framer-motion';
import { Shield, Key, Users } from 'lucide-react';

export const Security = () => {
  return (
    <section className="py-24 bg-background" id="security">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col lg:flex-row gap-16 items-center">
          <div className="lg:w-1/2">
            <motion.h2
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="text-3xl md:text-5xl font-semibold tracking-tight mb-6"
            >
              Security isn't an add-on.<br />
              <span className="text-white/50">It's the engine.</span>
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-lg text-muted-foreground mb-8"
            >
              Access to a document is granted only when all three conditions hold. The RBAC model is explicit, restrictive by default, and auditable.
            </motion.p>

            <div className="space-y-6">
              {[
                {
                  icon: <Users className="w-5 h-5 text-blue-400" />,
                  title: "1. Department Matching",
                  desc: "The document's department must be in the user's allowed departments (or Admin `*`)."
                },
                {
                  icon: <Shield className="w-5 h-5 text-purple-400" />,
                  title: "2. Clearance Levels",
                  desc: "Document sensitivity must be ≤ role clearance (public < internal < confidential < restricted)."
                },
                {
                  icon: <Key className="w-5 h-5 text-yellow-400" />,
                  title: "3. Explicit ACLs",
                  desc: "If a document declares `allowed_roles`, the user's role must be explicitly listed."
                }
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  className="flex gap-4 p-4 rounded-xl border border-white/5 bg-white/[0.02]"
                >
                  <div className="mt-1">{item.icon}</div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">{item.title}</h4>
                    <p className="text-sm text-muted-foreground">{item.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="lg:w-1/2 w-full">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="glass-card rounded-2xl p-6 md:p-8 border-white/10"
            >
              <h4 className="text-sm font-semibold text-white mb-6 uppercase tracking-wider">Access Policy Matrix</h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead>
                    <tr className="border-b border-white/10 text-muted-foreground">
                      <th className="pb-3 font-medium">Role</th>
                      <th className="pb-3 font-medium">Departments</th>
                      <th className="pb-3 font-medium">Clearance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    <tr>
                      <td className="py-3 font-medium text-white">Admin</td>
                      <td className="py-3 text-muted-foreground font-mono">*</td>
                      <td className="py-3 text-danger font-mono">restricted</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-medium text-white">HR</td>
                      <td className="py-3 text-muted-foreground font-mono">HR</td>
                      <td className="py-3 text-yellow-400 font-mono">confidential</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-medium text-white">Finance</td>
                      <td className="py-3 text-muted-foreground font-mono">Finance</td>
                      <td className="py-3 text-yellow-400 font-mono">confidential</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-medium text-white">Engineering</td>
                      <td className="py-3 text-muted-foreground font-mono">Engineering, Ops</td>
                      <td className="py-3 text-yellow-400 font-mono">confidential</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-medium text-white">Compliance</td>
                      <td className="py-3 text-muted-foreground font-mono">all (read)</td>
                      <td className="py-3 text-danger font-mono">restricted</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
};