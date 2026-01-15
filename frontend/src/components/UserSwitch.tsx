import React, { useState } from 'react';
import { User } from 'lucide-react';
import { useUser } from '../context/UserContext';

export const UserSwitch = ({ align = 'right' }: { align?: 'left' | 'right' }) => {
    const { username, switchUser } = useUser();
    const [isOpen, setIsOpen] = useState(false);
    const [inputName, setInputName] = useState('');

    // Load saved accounts from local storage, fallback to defaults
    const [savedUsers, setSavedUsers] = useState<string[]>(() => {
        try {
            const stored = localStorage.getItem('aichef_saved_users');
            // Merge defaults using Set to avoid duplicates
            const defaults = ['Dad', 'Mom', 'Kid'];
            if (stored) {
                const parsed = JSON.parse(stored);
                return Array.from(new Set([...defaults, ...parsed]));
            }
            return defaults;
        } catch {
            return ['Dad', 'Mom', 'Kid'];
        }
    });

    const handleSwitch = (e: React.FormEvent) => {
        e.preventDefault();
        const trimmed = inputName.trim();
        if (trimmed) {
            // Add to saved users if new
            if (!savedUsers.includes(trimmed)) {
                const newUsers = [...savedUsers, trimmed];
                setSavedUsers(newUsers);
                localStorage.setItem('aichef_saved_users', JSON.stringify(newUsers));
            }

            switchUser(trimmed);
            setIsOpen(false);
            setInputName('');
        }
    };

    return (
        <div className="relative z-50">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur border border-slate-200 rounded-full text-slate-700 hover:bg-white hover:shadow-md transition-all shadow-sm"
            >
                <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-orange-600">
                    <User size={14} />
                </div>
                <span className="text-sm font-medium pr-1">{username}</span>
            </button>

            {isOpen && (
                <div className={`absolute top-12 w-64 bg-white rounded-xl shadow-xl border border-slate-100 p-4 animate-in fade-in slide-in-from-top-2 ${align === 'left' ? 'left-0' : 'right-0'
                    }`}>
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Switch Profile</h3>

                    <div className="space-y-2 mb-4 max-h-48 overflow-y-auto">
                        {/* Always show "default" plus saved users */}
                        {Array.from(new Set(['default', ...savedUsers])).map(name => (
                            <button
                                key={name}
                                onClick={() => switchUser(name)}
                                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${username === name
                                    ? 'bg-orange-50 text-orange-700 font-medium'
                                    : 'hover:bg-slate-50 text-slate-600'
                                    }`}
                            >
                                {name}
                            </button>
                        ))}
                    </div>

                    <form onSubmit={handleSwitch} className="pt-3 border-t border-slate-50">
                        <label className="text-xs text-slate-500 mb-1 block">Or enter new name:</label>
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={inputName}
                                onChange={e => setInputName(e.target.value)}
                                className="flex-1 px-2 py-1.5 text-sm border border-slate-200 rounded-md focus:outline-none focus:border-orange-500"
                                placeholder="Name..."
                            />
                            <button type="submit" className="px-3 py-1.5 bg-slate-800 text-white text-xs rounded-md">
                                Go
                            </button>
                        </div>
                    </form>
                </div>
            )}
        </div>
    );
};
