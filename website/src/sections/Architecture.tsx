
import { motion } from 'framer-motion';
import { Network, Server, Lock, Cpu } from 'lucide-react';

export function Architecture() {
  return (
    <section id="architecture" className="py-24 bg-muted/30 border-y border-border/50">
      <div className="container px-4 mx-auto">
        <div className="flex flex-col lg:flex-row gap-16 items-center">

          <div className="w-full lg:w-1/2 space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Uncompromising Architecture</h2>
              <p className="text-lg text-muted-foreground">
                Built from the ground up for security, speed, and reliability. We run where you need us, integrating seamlessly into your existing infrastructure.
              </p>
            </motion.div>

            <div className="space-y-6">
              {[
                { title: 'VPC Deployment', desc: 'Deploy within your own secure VPC. No data ever leaves your network perimeter.', icon: Lock },
                { title: 'Scalable Ingestion', desc: 'Distributed document parsing and embedding pipelines handle petabytes of data.', icon: Server },
                { title: 'Agentic Orchestration', desc: 'LangGraph powers intelligent routing, multi-step reasoning, and tool execution.', icon: Network }
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="flex gap-4"
                >
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                    <item.icon className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold">{item.title}</h4>
                    <p className="text-muted-foreground">{item.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          <motion.div
            className="w-full lg:w-1/2"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
          >
            <div className="relative aspect-square md:aspect-video lg:aspect-square bg-card border border-border/50 rounded-2xl shadow-2xl p-8 overflow-hidden flex flex-col justify-between">
              <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

              <div className="relative z-10 flex justify-between items-start w-full">
                <div className="bg-background/80 backdrop-blur border border-border px-4 py-2 rounded-lg text-sm font-mono flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-primary" /> Edge Network
                </div>
                <div className="bg-background/80 backdrop-blur border border-border px-4 py-2 rounded-lg text-sm font-mono">
                  Enterprise DB
                </div>
              </div>

              <div className="relative z-10 flex justify-center items-center h-full">
                <div className="w-32 h-32 rounded-full border border-primary/30 flex items-center justify-center bg-primary/5 animate-[spin_10s_linear_infinite]">
                  <div className="w-24 h-24 rounded-full border border-primary/50 flex items-center justify-center border-dashed bg-primary/10">
                     <Lock className="w-8 h-8 text-primary animate-[spin_10s_linear_infinite_reverse]" />
                  </div>
                </div>
              </div>

               <div className="relative z-10 w-full text-center text-sm text-muted-foreground font-mono bg-background/80 backdrop-blur border border-border p-3 rounded-lg">
                 End-to-End Encryption Enabled
               </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
