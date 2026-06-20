import { motion } from 'framer-motion';
import { Book, Code, Terminal, ArrowRight } from 'lucide-react';
import { Button } from '../components/Button';

export const Documentation = () => {
  return (
    <section className="py-24 bg-background relative border-y border-white/5" id="docs">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center gap-12">
          <div className="flex-1">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-3xl md:text-5xl font-semibold tracking-tight mb-6"
            >
              Developer-first documentation.
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-lg text-muted-foreground mb-8"
            >
              Everything you need to integrate, deploy, and manage Kortex. Comprehensive guides, API references, and architecture blueprints.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
            >
              <Button variant="secondary" className="gap-2">
                Browse Documentation <ArrowRight className="w-4 h-4" />
              </Button>
            </motion.div>
          </div>

          <div className="flex-1 w-full grid gap-4">
            {[
              { icon: <Terminal className="w-5 h-5 text-green-400" />, title: "Quickstart Guide", desc: "Get up and running locally in 5 minutes." },
              { icon: <Code className="w-5 h-5 text-blue-400" />, title: "API Reference", desc: "Detailed endpoints for querying and ingestion." },
              { icon: <Book className="w-5 h-5 text-orange-400" />, title: "Architecture Blueprints", desc: "Deployment patterns for AWS, GCP, and Azure." }
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3 + i * 0.1 }}
                className="glass-card p-6 rounded-xl border border-white/10 flex items-start gap-4 hover:bg-white/5 transition-colors cursor-pointer group"
              >
                <div className="p-2 bg-white/5 rounded-lg group-hover:scale-110 transition-transform">
                  {item.icon}
                </div>
                <div>
                  <h4 className="font-semibold">{item.title}</h4>
                  <p className="text-sm text-muted-foreground">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
