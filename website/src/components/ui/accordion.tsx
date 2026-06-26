import * as React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { ChevronDownIcon } from "lucide-react"
import { cn } from "../../lib/utils"

interface AccordionItem {
  id: string
  title: string
  content: React.ReactNode
}

interface AccordionProps {
  items: AccordionItem[]
  className?: string
}

export function Accordion({ items, className }: AccordionProps) {
  const [openItem, setOpenItem] = React.useState<string | null>(null)

  return (
    <div className={cn("w-full space-y-2", className)} role="region" aria-label="Accordion">
      {items.map((item) => {
        const isOpen = openItem === item.id
        return (
          <div key={item.id} className="border-b border-border last:border-0 overflow-hidden">
            <button
              onClick={() => setOpenItem(isOpen ? null : item.id)}
              className="flex w-full items-center justify-between py-4 text-left text-sm font-medium transition-all hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              aria-expanded={isOpen}
              aria-controls={`accordion-content-${item.id}`}
              id={`accordion-trigger-${item.id}`}
            >
              {item.title}
              <ChevronDownIcon
                className={cn(
                  "h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200",
                  isOpen && "rotate-180"
                )}
              />
            </button>
            <AnimatePresence initial={false}>
              {isOpen && (
                <motion.div
                  key="content"
                  initial="collapsed"
                  animate="open"
                  exit="collapsed"
                  variants={{
                    open: { opacity: 1, height: "auto" },
                    collapsed: { opacity: 0, height: 0 },
                  }}
                  transition={{ duration: 0.3, ease: [0.04, 0.62, 0.23, 0.98] }}
                  id={`accordion-content-${item.id}`}
                  role="region"
                  aria-labelledby={`accordion-trigger-${item.id}`}
                >
                  <div className="pb-4 pt-0 text-sm text-muted-foreground">
                    {item.content}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )
      })}
    </div>
  )
}
