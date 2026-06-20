import { motion } from 'framer-motion';
import { Zap, Activity, Clock } from 'lucide-react';

export const Performance = () => {
  return (
    <section className="py-24 bg-background relative" id="performance">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            Built for speed. <span className="text-muted-foreground">Engineered for scale.</span>
          </motion.h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: <Zap className="w-6 h-6 text-yellow-400" />,
              stat: "< 50ms",
              label: "Average Retrieval Latency",
              desc: "Lightning-fast semantic search powered by optimized vector indexing."
            },
            {
              icon: <Activity className="w-6 h-6 text-green-400" />,
              stat: "99.99%",
              label: "Uptime SLA",
              desc: "Enterprise-grade reliability with resilient, high-availability infrastructure."
            },
            {
              icon: <Clock className="w-6 h-6 text-blue-400" />,
              stat: "10M+",
              label: "Documents Processed / Hour",
              desc: "Massively parallel ingestion pipeline handles enterprise data volume with ease."
            }
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass-card p-8 rounded-2xl border border-white/5 text-center flex flex-col items-center"
            >
              <div className="mb-4 p-3 bg-white/5 rounded-full inline-block">
                {item.icon}
              </div>
              <div className="text-4xl font-bold mb-2 tracking-tight">{item.stat}</div>
              <div className="text-lg font-medium text-foreground/80 mb-2">{item.label}</div>
              <p className="text-muted-foreground text-sm">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
