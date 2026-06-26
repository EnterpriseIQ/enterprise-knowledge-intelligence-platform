
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Accordion } from '../components/ui/accordion';

export function FaqCta() {
  const faqs = [
    {
      id: "1",
      title: "Does EnterpriseIq support air-gapped environments?",
      content: "Yes. EnterpriseIq is designed for strict enterprise security requirements. You can deploy the entire platform, including local LLMs like Llama 3 or Qwen, entirely offline within your VPC."
    },
    {
      id: "2",
      title: "How does RBAC work at the document chunk level?",
      content: "During ingestion, document permissions from your source systems (like Confluence or Jira) are mapped to metadata. Our retrieval engine strictly filters vectors based on the requesting user's identity before they are sent to the LLM."
    },
    {
      id: "3",
      title: "What is the difference between dense vector search and hybrid search?",
      content: "Dense vector search captures semantic meaning, but struggles with exact keywords (like IDs or product names). EnterpriseIq uses Hybrid Search, combining dense vectors with sparse BM25 keyword search, and reranks them with a Cross-Encoder for maximum accuracy."
    },
    {
      id: "4",
      title: "Can I use my own fine-tuned models?",
      content: "Absolutely. The platform is model-agnostic. You can plug in custom embedding models, rerankers, and LLMs via our extensible architecture."
    }
  ];

  return (
    <>
      <section className="py-24 bg-muted/20 border-y border-border/50">
        <div className="container px-4 mx-auto max-w-3xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Frequently Asked Questions</h2>
            <p className="text-muted-foreground">Everything you need to know about the product and billing.</p>
          </div>
          <Accordion items={faqs} />
        </div>
      </section>

      <section className="py-32 relative overflow-hidden">
        <div className="absolute inset-0 bg-primary/5"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/20 rounded-full blur-[120px] opacity-50 pointer-events-none"></div>

        <div className="container px-4 mx-auto relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-2xl mx-auto"
          >
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">Ready to scale your enterprise AI?</h2>
            <p className="text-xl text-muted-foreground mb-10">
              Build secure, reliable, and high-performance agentic workflows.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="gap-2 rounded-full h-12 px-8 text-base shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)]">
                Start Building Today
                <ArrowRight className="w-4 h-4" />
              </Button>
              <Button size="lg" variant="outline" className="gap-2 rounded-full h-12 px-8 text-base bg-background/50 backdrop-blur-sm">
                Contact Sales
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </>
  );
}
