import { motion } from 'framer-motion';
import { Terminal, Copy, Check } from 'lucide-react';
import { useState } from 'react';

export const DevExperience = () => {
  const [copied, setCopied] = useState(false);
  const code = `git clone https://github.com/enterpriseiq/enterprise-knowledge-intelligence-platform.git
cd enterprise-knowledge-intelligence-platform

# Generate the synthetic enterprise corpus
python -m data.generate_data

# Run the end-to-end demo and RBAC proof
python run_demo.py

# Start the offline-first API
uvicorn src.api.main:app --reload`;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="py-24 bg-background relative overflow-hidden" id="developers">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-white/[0.02]" />

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <motion.h2
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="text-3xl md:text-5xl font-semibold tracking-tight mb-6"
            >
              Deploys in minutes.<br />
              <span className="text-white/50">Adapts to your stack.</span>
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-lg text-muted-foreground mb-8"
            >
              Kortex is built for engineers. It ships as a slim, non-root Docker container, configured via twelve-factor environment variables, exposing a fully typed FastAPI backend.
            </motion.p>

            <ul className="space-y-4">
              {[
                "100% Offline Capable",
                "Typed Python FastAPI",
                "Docker & CI Ready",
                "Built-in Synthetic Data Generator"
              ].map((feature, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  className="flex items-center gap-3 text-white"
                >
                  <div className="w-1.5 h-1.5 rounded-full bg-success" />
                  {feature}
                </motion.li>
              ))}
            </ul>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="rounded-xl border border-white/10 bg-[#0A0A0A] overflow-hidden shadow-2xl relative"
          >
            <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-white/5">
              <div className="flex items-center gap-2 text-xs text-muted-foreground font-mono">
                <Terminal className="w-4 h-4" /> Quickstart
              </div>
              <button
                onClick={handleCopy}
                className="text-muted-foreground hover:text-white transition-colors"
                aria-label="Copy code"
              >
                {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
            <div className="p-6 overflow-x-auto">
              <pre className="text-sm font-mono leading-relaxed">
                <code className="text-muted-foreground">
                  {code.split('\n').map((line, i) => (
                    <div key={i}>
                      {line.startsWith('#') ? (
                        <span className="text-gray-500">{line}</span>
                      ) : line ? (
                        <>
                          <span className="text-blue-400 mr-2">$</span>
                          <span className="text-white">{line}</span>
                        </>
                      ) : (
                        <br />
                      )}
                    </div>
                  ))}
                </code>
              </pre>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};