import { motion } from 'framer-motion';
import { Database, ShieldAlert, FileX } from 'lucide-react';

export const Problem = () => {
  return (
    <section className="py-24 bg-background relative overflow-hidden" id="problem">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            Your data is siloed. <br className="hidden md:block" />
            <span className="text-danger">Naive AI makes it dangerous.</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-lg text-muted-foreground max-w-2xl mx-auto"
          >
            Giving an LLM unconstrained access to your enterprise data is a data leak waiting to happen. Hallucinations erode trust, and weak access controls lead to compliance breaches.
          </motion.p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: <Database className="w-6 h-6 text-orange-400" />,
              title: "Information Silos",
              desc: "Critical knowledge is fragmented across PDFs, SQL databases, CSVs, and JSON logs. Employees waste hours manually hunting across disconnected systems."
            },
            {
              icon: <ShieldAlert className="w-6 h-6 text-danger" />,
              title: "Access Control Failures",
              desc: "Standard RAG embeds everything and retrieves nearest neighbors. A naive system will happily quote a restricted finance document to an unauthorized engineer."
            },
            {
              icon: <FileX className="w-6 h-6 text-yellow-400" />,
              title: "Hallucinated Answers",
              desc: "Confident, incorrect answers erode user trust. Without strict extractive grounding and verifiable citations, the AI is guessing rather than reasoning."
            }
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 + i * 0.1 }}
              className="glass-card p-8 rounded-2xl border border-white/10 hover:border-white/20 transition-colors relative group"
            >
              <div className="mb-4 p-3 bg-white/5 rounded-lg inline-block group-hover:scale-110 transition-transform">
                {item.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3">{item.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};