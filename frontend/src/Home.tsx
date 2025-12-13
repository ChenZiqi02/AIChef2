import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Beef, Fish, Carrot, Coffee, ChefHat, Heart } from 'lucide-react';

const HomePage = () => {
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            navigate(`/results?q=${encodeURIComponent(query)}`);
        }
    };

    const categories = [
        { name: "Signature Meats", icon: <Beef size={28} />, query: "肉类料理" },
        { name: "Ocean Fresh", icon: <Fish size={28} />, query: "海鲜" },
        { name: "Garden Greens", icon: <Carrot size={28} />, query: "素食" },
        { name: "Morning Delights", icon: <Coffee size={28} />, query: "早餐" },
    ];

    return (
        <div className="min-h-screen bg-stone-50 font-sans selection:bg-orange-100 selection:text-orange-900">
            {/* Navigation */}
            <nav className="absolute top-0 left-0 right-0 p-6 flex justify-between items-center z-10">
                <div className="flex items-center gap-2 opacity-0 pointer-events-none md:opacity-100">
                    {/* Placeholder for balance */}
                </div>
                <button
                    onClick={() => navigate('/favorites')}
                    className="flex items-center gap-2 px-5 py-2 bg-white/50 backdrop-blur-md hover:bg-white border border-stone-200 rounded-full text-stone-600 hover:text-orange-600 transition-all shadow-sm font-medium text-sm tracking-wide"
                >
                    <Heart size={16} />
                    <span>MY COLLECTION</span>
                </button>
            </nav>

            <div className="min-h-screen flex flex-col items-center justify-center p-4 relative">
                {/* Decorative Background Elements */}
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-orange-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob" />
                <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-yellow-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000" />

                <div className="w-full max-w-4xl space-y-16 text-center relative z-10">

                    {/* Header */}
                    <div className="flex flex-col items-center space-y-6">
                        <div className="p-6 bg-white rounded-full text-orange-600 shadow-xl shadow-orange-100 mb-4 border border-orange-50">
                            <ChefHat size={64} strokeWidth={1.5} />
                        </div>
                        <div>
                            <h1 className="text-5xl md:text-7xl font-bold text-stone-800 tracking-tight font-serif mb-4">
                                AIChef <span className="text-orange-600">.</span>
                            </h1>
                            <p className="text-xl text-stone-500 font-light tracking-wide max-w-lg mx-auto leading-relaxed">
                                Your personal culinary consultant. <br />Turn simple ingredients into gourmet experiences.
                            </p>
                        </div>
                    </div>

                    {/* Search Bar */}
                    <form onSubmit={handleSearch} className="relative group max-w-2xl mx-auto">
                        <div className="absolute inset-y-0 left-0 pl-8 flex items-center pointer-events-none">
                            <Search className="h-6 w-6 text-stone-400 group-focus-within:text-orange-500 transition-colors" />
                        </div>
                        <input
                            type="text"
                            className="w-full pl-20 pr-8 py-6 text-xl rounded-full border-2 border-stone-100 bg-white shadow-lg shadow-stone-200/50 focus:ring-0 focus:border-orange-200 outline-none transition-all placeholder:text-stone-300 font-serif"
                            placeholder="Enter your available ingredients..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <button
                            type="submit"
                            className="absolute right-3 top-2.5 bottom-2.5 px-6 bg-stone-900 text-white rounded-full font-medium hover:bg-orange-600 transition-colors"
                        >
                            Consult
                        </button>
                    </form>

                    {/* Categories */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        {categories.map((cat) => (
                            <button
                                key={cat.name}
                                onClick={() => navigate(`/results?q=${encodeURIComponent(cat.query)}`)}
                                className="flex flex-col items-center justify-center p-8 bg-white rounded-2xl border border-stone-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-500 group"
                            >
                                <div className="text-stone-300 group-hover:text-orange-500 transition-colors duration-500 mb-4 transform group-hover:scale-110">
                                    {cat.icon}
                                </div>
                                <span className="font-medium text-stone-600 group-hover:text-stone-900 font-serif tracking-wide">{cat.name}</span>
                            </button>
                        ))}
                    </div>

                </div>
            </div>

            {/* Footer */}
            <div className="absolute bottom-6 left-0 right-0 text-center text-stone-300 text-sm font-light tracking-widest uppercase">
                Fine Dining at Home
            </div>
        </div>
    );
};

export default HomePage;
