import { motion } from 'framer-motion';
import { Button } from '../components/Button';
import { ArrowRight } from 'lucide-react';

export const CTA = () => {
  return (
    <section className="py-32 relative overflow-hidden">
      <div className="absolute inset-0 bg-hero-glow opacity-20 blur-[150px] mix-blend-screen pointer-events-none" />

      <div className="max-w-4xl mx-auto px-6 relative z-10 text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-4xl md:text-6xl font-semibold tracking-tight mb-6"
        >
          Ready to unlock your <br /> enterprise knowledge?
        </motion.h2>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto"
        >
          Stop compromising between security and intelligence. Deploy Kortex today and give your team the answers they need, safely.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="flex flex-col sm:flex-row justify-center gap-4"
        >
          <Button size="lg" className="group text-lg h-14 px-8">
            Deploy Local Version
            <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button size="lg" variant="outline" className="text-lg h-14 px-8 bg-white/5">
            Read the Architecture Spec
          </Button>
        </motion.div>
      </div>
    </section>
  );
};