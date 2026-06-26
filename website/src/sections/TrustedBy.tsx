
import { motion } from 'framer-motion';

export function TrustedBy() {
  const logos = [
    { name: 'Vercel', icon: '▲' },
    { name: 'Linear', icon: '◮' },
    { name: 'Raycast', icon: '✧' },
    { name: 'Stripe', icon: '///' },
    { name: 'OpenAI', icon: '✿' }
  ];

  return (
    <section className="py-12 border-y border-border/50 bg-muted/20">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm font-medium text-muted-foreground mb-8 uppercase tracking-widest">
          Trusted by innovative engineering teams
        </p>
        <div className="flex flex-wrap justify-center gap-8 md:gap-16 items-center opacity-70 grayscale">
          {logos.map((logo, i) => (
            <motion.div
              key={logo.name}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="flex items-center gap-2 text-xl font-bold text-foreground/80 hover:text-foreground transition-colors cursor-default"
            >
              <span className="text-2xl">{logo.icon}</span>
              {logo.name}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
