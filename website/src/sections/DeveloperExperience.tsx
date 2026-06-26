
import { motion } from 'framer-motion';
import { Code2, Terminal, Blocks } from 'lucide-react';
import { Card } from '../components/ui/card';

export function DeveloperExperience() {

  return (
    <section id="docs" className="py-24 relative">
      <div className="container px-4 mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Loved by Developers.</h2>
          <p className="text-lg text-muted-foreground">
            A world-class developer experience with strongly-typed SDKs, comprehensive documentation, and predictable APIs.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 items-center">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="relative rounded-xl border border-border bg-[#0d1117] overflow-hidden shadow-2xl"
          >
            <div className="flex items-center px-4 py-3 border-b border-border/50 bg-[#161b22]">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
                <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
                <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
              </div>
              <div className="mx-auto text-xs font-mono text-muted-foreground">query.ts</div>
            </div>
            <div className="p-6 overflow-x-auto">
              <pre className="text-sm font-mono leading-relaxed">
                <code className="text-[#c9d1d9]">
                  <span className="text-[#ff7b72]">import</span> {'{'} <span className="text-[#79c0ff]">KnowledgeX</span> {'}'} <span className="text-[#ff7b72]">from</span> <span className="text-[#a5d6ff]">'@knowledgex/sdk'</span>;<br/><br/>
                  <span className="text-[#ff7b72]">const</span> <span className="text-[#79c0ff]">client</span> <span className="text-[#ff7b72]">=</span> <span className="text-[#ff7b72]">new</span> <span className="text-[#d2a8ff]">KnowledgeX</span>({'{'}<br/>
                  {'  '}apiKey: <span className="text-[#79c0ff]">process</span>.env.<span className="text-[#79c0ff]">KX_API_KEY</span>,<br/>
                  {'  '}environment: <span className="text-[#a5d6ff]">'production'</span><br/>
                  {'}'});<br/><br/>
                  <span className="text-[#8b949e]">// Execute an agentic query with strict RBAC</span><br/>
                  <span className="text-[#ff7b72]">const</span> <span className="text-[#79c0ff]">response</span> <span className="text-[#ff7b72]">= await</span> client.agents.<span className="text-[#d2a8ff]">execute</span>({'{'}<br/>
                  {'  '}query: <span className="text-[#a5d6ff]">"Summarize the Q3 internal security audit"</span>,<br/>
                  {'  '}userId: <span className="text-[#a5d6ff]">"user_123"</span>,<br/>
                  {'  '}options: {'{'}<br/>
                  {'    '}reranker: <span className="text-[#a5d6ff]">"cross-encoder"</span>,<br/>
                  {'    '}useHybridSearch: <span className="text-[#79c0ff]">true</span><br/>
                  {'  }'}<br/>
                  {'}'});
                </code>
              </pre>
            </div>
          </motion.div>

          <div className="space-y-6 lg:pl-12">
            {[
              { icon: Code2, title: 'Type-Safe SDKs', desc: 'First-class support for TypeScript, Python, and Go.' },
              { icon: Terminal, title: 'CLI Tooling', desc: 'Manage indexes, test queries, and deploy agents from your terminal.' },
              { icon: Blocks, title: 'Extensible Framework', desc: 'Build custom retrievers and agent tools with ease.' }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Card className="p-6 bg-card/50 border-border/50 hover:bg-card transition-colors">
                  <div className="flex gap-4">
                    <div className="mt-1">
                      <feature.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h4 className="text-lg font-semibold">{feature.title}</h4>
                      <p className="text-muted-foreground mt-1">{feature.desc}</p>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
