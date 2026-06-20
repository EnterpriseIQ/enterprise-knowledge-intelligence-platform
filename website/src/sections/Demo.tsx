import { motion } from 'framer-motion';

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
          <div className="aspect-[16/9] bg-[#0A0A0A] rounded-2xl border border-white/10 shadow-2xl overflow-hidden flex items-center justify-center relative group cursor-pointer">
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/10 to-blue-500/10 pointer-events-none" />

            {/* Mock Dashboard UI */}
            <div className="w-full h-full flex flex-col p-4 opacity-80">
              {/* Header */}
              <div className="flex items-center gap-2 mb-6 border-b border-white/5 pb-4">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
                <div className="ml-4 h-6 w-64 bg-white/5 rounded" />
              </div>
              {/* Body */}
              <div className="flex-1 flex gap-6">
                {/* Sidebar */}
                <div className="w-48 flex flex-col gap-3 hidden sm:flex border-r border-white/5 pr-4">
                  <div className="h-6 w-full bg-white/5 rounded" />
                  <div className="h-6 w-3/4 bg-white/5 rounded" />
                  <div className="h-6 w-5/6 bg-white/5 rounded" />
                </div>
                {/* Main Content */}
                <div className="flex-1 flex flex-col gap-4">
                  <div className="h-32 w-full bg-white/5 rounded-xl border border-white/5" />
                  <div className="h-12 w-3/4 bg-white/5 rounded-xl border border-white/5" />
                  <div className="h-12 w-full bg-white/5 rounded-xl border border-white/5" />
                </div>
              </div>
            </div>

            {/* Play Button Overlay */}
            <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-[2px]">
               <div className="w-16 h-16 rounded-full bg-white text-black flex items-center justify-center pl-1 shadow-xl">
                 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
               </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
