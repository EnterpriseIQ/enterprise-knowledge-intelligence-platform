import { motion } from 'framer-motion';
import { CheckCircle2, Lock, FileText, Database } from 'lucide-react';

export const Solution = () => {
  return (
    <section className="py-24 relative overflow-hidden bg-white/[0.01]" id="solution">
      <div className="absolute top-1/2 right-0 -translate-y-1/2 w-[600px] h-[600px] bg-success/10 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
        <div>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-6"
          >
            Grounded answers. <br />
            <span className="text-success">Governed access.</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-lg text-muted-foreground mb-8"
          >
            EnterpriseIq enforces strict Role-Based Access Control (RBAC) <em>before</em> generating answers. Every query is filtered through a rigorous clearance matrix, ensuring complete compliance and exact citations.
          </motion.p>

          <ul className="space-y-6">
            {[
              {
                icon: <Lock className="w-5 h-5 text-success" />,
                title: "Defence-in-Depth Retrieval",
                desc: "Documents inherit security metadata. RBAC is enforced as a vector pre-filter and a post-retrieval check."
              },
              {
                icon: <FileText className="w-5 h-5 text-success" />,
                title: "Zero Hallucination Guarantee",
                desc: "Answers are generated purely extractively. If there's insufficient evidence, the platform refuses rather than guesses."
              },
              {
                icon: <CheckCircle2 className="w-5 h-5 text-success" />,
                title: "Complete Traceability",
                desc: "Every response includes routing rationale, access decision logs, and exact inline citations mapped to source documents."
              }
            ].map((item, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 + i * 0.1 }}
                className="flex gap-4"
              >
                <div className="mt-1 bg-success/10 p-2 rounded-lg h-fit">{item.icon}</div>
                <div>
                  <h4 className="font-semibold text-white mb-1">{item.title}</h4>
                  <p className="text-muted-foreground text-sm leading-relaxed">{item.desc}</p>
                </div>
              </motion.li>
            ))}
          </ul>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="relative"
        >
          <div className="glass-card rounded-2xl p-8 border border-white/10 hover:border-white/20 transition-colors bg-success/[0.02]">
             <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-blue-400" />
                    <div>
                      <div className="text-sm font-medium">Engineering_Specs.pdf</div>
                      <div className="text-xs text-muted-foreground">Clearance: Internal</div>
                    </div>
                  </div>
                  <div className="text-xs font-mono text-success bg-success/10 px-2 py-1 rounded">ALLOW</div>
                </div>

                <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10 opacity-50 grayscale">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-green-400" />
                    <div>
                      <div className="text-sm font-medium">Q3_Executive_Salaries.csv</div>
                      <div className="text-xs text-muted-foreground">Clearance: Restricted</div>
                    </div>
                  </div>
                  <div className="text-xs font-mono text-danger bg-danger/10 px-2 py-1 rounded">DENY: INSUFFICIENT CLEARANCE</div>
                </div>

                <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10">
                  <div className="flex items-center gap-3">
                    <Database className="w-5 h-5 text-purple-400" />
                    <div>
                      <div className="text-sm font-medium">API_Access_Logs.json</div>
                      <div className="text-xs text-muted-foreground">Clearance: Public</div>
                    </div>
                  </div>
                  <div className="text-xs font-mono text-success bg-success/10 px-2 py-1 rounded">ALLOW</div>
                </div>
             </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};