import { motion } from 'framer-motion';
import { Database, Search, Cpu, CheckCircle } from 'lucide-react';

export const HowItWorks = () => {
  const steps = [
    {
      icon: <Database className="w-6 h-6 text-blue-400" />,
      title: "1. Connect Data Sources",
      description: "Securely connect your fragmented data repositories. Kortex creates an intelligent graph of your enterprise knowledge."
    },
    {
      icon: <Search className="w-6 h-6 text-purple-400" />,
      title: "2. Query the Knowledge Graph",
      description: "Users ask complex questions. Kortex searches through structured and unstructured data in milliseconds."
    },
    {
      icon: <Cpu className="w-6 h-6 text-orange-400" />,
      title: "3. Agentic RAG Processing",
      description: "Advanced reasoning agents retrieve the right context, rerank results, and enforce strict access controls."
    },
    {
      icon: <CheckCircle className="w-6 h-6 text-green-400" />,
      title: "4. Receive Trusted Answers",
      description: "Get perfectly cited, hallucination-free answers derived exclusively from your enterprise data."
    }
  ];

  return (
    <section className="py-24 bg-background relative overflow-hidden" id="how-it-works">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            How it works
          </motion.h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            A seamless pipeline from unstructured data to precise intelligence.
          </p>
        </div>

        <div className="grid md:grid-cols-4 gap-8">
          {steps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="relative"
            >
              <div className="mb-6 p-4 bg-white/5 inline-block rounded-xl border border-white/10">
                {step.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3">{step.title}</h3>
              <p className="text-muted-foreground">{step.description}</p>

              {/* Connector line for large screens */}
              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-10 left-20 w-full h-[1px] bg-gradient-to-r from-white/20 to-transparent" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
