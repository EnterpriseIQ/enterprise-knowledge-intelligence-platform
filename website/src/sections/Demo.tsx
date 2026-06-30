import { motion } from 'framer-motion';
import { QueryForm } from '../components/QueryForm';

export const Demo = () => {
  return (
    <section className="py-24 bg-background relative overflow-hidden" id="demo">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            See Kortex in Action
          </motion.h2>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative max-w-5xl mx-auto"
        >
          <div className="h-[600px] w-full bg-[#0A0A0A] rounded-2xl border border-white/10 shadow-2xl overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/5 to-blue-500/5 pointer-events-none" />
            <QueryForm />
          </div>
        </motion.div>
      </div>
    </section>
  );
};
