import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Sparkles } from 'lucide-react';

const GrokInsight = ({ insight, prediction }) => {
    if (!insight) return null;

    const isPositive = prediction > 0;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="glass-panel p-6 mt-6 border-l-4 border-l-purple-500"
            >
                <div className="flex items-start gap-4">
                    <div className="p-3 bg-purple-500/20 rounded-full animate-pulse-glow">
                        <Bot className="text-purple-400" size={32} />
                    </div>

                    <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                            <h3 className="text-lg font-bold gradient-text">Grok's Take</h3>
                            <Sparkles size={16} className="text-yellow-400" />
                        </div>

                        <p className="text-gray-300 text-lg leading-relaxed italic">
                            "{insight}"
                        </p>

                        <div className="mt-4 flex items-center gap-2">
                            <span className="text-xs uppercase tracking-wider text-gray-500">Confidence Level:</span>
                            <div className="h-2 flex-1 bg-slate-700 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${Math.min(Math.abs(prediction) * 10 + 50, 95)}%` }}
                                    className={`h-full ${isPositive ? 'bg-green-500' : 'bg-red-500'}`}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
};

export default GrokInsight;
