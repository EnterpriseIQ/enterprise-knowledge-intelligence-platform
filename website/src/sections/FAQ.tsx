import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

const faqs = [
  {
    q: "How does Kortex differ from standard RAG?",
    a: "Standard RAG assumes all embedded documents can be read by anyone. Kortex treats access control as a first-class retrieval concern, filtering vectors by clearance and explicit ACLs before they can ever reach the generation phase."
  },
  {
    q: "Does it require an internet connection?",
    a: "No. While it supports external providers like OpenAI and Anthropic, Kortex defaults to a completely offline stack using local sentence-transformers, ChromaDB, and local LLMs (like Qwen3 or Llama 3 via Ollama) to guarantee absolute data privacy."
  },
  {
    q: "How does it handle unstructured vs structured data?",
    a: "Kortex maps heterogeneous data (PDFs, CSVs, SQL rows, JSON logs) into a unified `RawDocument` model during ingestion, allowing a single hybrid search query to retrieve and rank context across all source types simultaneously."
  },
  {
    q: "What prevents the AI from hallucinating?",
    a: "Kortex uses an 'Extractive Grounding' prompt technique. The LLM is strictly instructed to answer only using the provided retrieved context, and to explicitly refuse to answer if the context lacks sufficient evidence. Every claim is mapped to a cited source snippet."
  }
];

export const FAQ = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section className="py-24 bg-background" id="faq">
      <div className="max-w-3xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight"
          >
            Questions, answered.
          </motion.h2>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="border border-white/10 rounded-xl overflow-hidden glass-card"
            >
              <button
                id={`faq-question-${i}`}
                aria-expanded={openIndex === i}
                aria-controls={`faq-answer-${i}`}
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="w-full flex items-center justify-between p-6 text-left"
              >
                <span className="font-medium text-lg">{faq.q}</span>
                <ChevronDown
                  aria-hidden="true"
                  className={`w-5 h-5 text-muted-foreground transition-transform duration-300 ${openIndex === i ? 'rotate-180' : ''}`}
                />
              </button>
              <AnimatePresence>
                {openIndex === i && (
                  <motion.div
                    id={`faq-answer-${i}`}
                    role="region"
                    aria-labelledby={`faq-question-${i}`}
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="px-6 pb-6 text-muted-foreground leading-relaxed">
                      {faq.a}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};