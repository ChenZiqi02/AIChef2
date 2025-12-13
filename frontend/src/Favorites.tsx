import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, Gauge, Heart, ChefHat } from 'lucide-react';
import type { Recipe } from './types';
import axios from 'axios';

const FavoritesPage = () => {
    const navigate = useNavigate();
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadFavorites = async () => {
            const favIds = JSON.parse(localStorage.getItem('aichef_favorites') || '[]');
            if (favIds.length === 0) {
                setRecipes([]);
                setLoading(false);
                return;
            }

            try {
                // In a real backend we would have an endpoint like /api/recipes?ids=...
                // Only for demo: we simulate fetching by searching or handling ID individually 
                // Since our backend is limited, we might not be able to fetch details easily by ID list 
                // without n+1 calls. Let's try to fetch them one by one for now (optimization for later).

                // Note: The current backend /api/search returns 'candidates'. 
                // To fetch a specific recipe by ID, we might not have a direct endpoint yet.
                // However, the Detail page works by passing status. If we reload Detail page directly, does it work?
                // Actually the current Detail page relies on `location.state`. It crashes if refreshed.
                // WE NEED TO FIX THIS: To support Favorites properly, best is to store the *entire* recipe object in localStorage 
                // for this prototype, to avoid backend complexity of fetching by ID.

                // Let's check what Detail.tsx does. It saves ONLY ID.
                // Change of Plan: To make this robust without backend changes, let's load what we can.
                // BUT, if we only have ID, we can't show title/image easily.

                // ALTERNATIVE: Since we want a "high end" experience, let's assume valid data.
                // I'll update Detail.tsx to save the WHOLE recipe object to 'aichef_saved_recipes' map.

                const savedMap = JSON.parse(localStorage.getItem('aichef_saved_recipes') || '{}');
                const loadedRecipes = favIds.map((id: string) => savedMap[id]).filter(Boolean);
                setRecipes(loadedRecipes);

            } catch (err) {
                console.error("Failed to load favorites", err);
            } finally {
                setLoading(false);
            }
        };

        loadFavorites();
    }, []);

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Header */}
            <header className="bg-white border-b border-slate-100 sticky top-0 z-10">
                <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
                    <button onClick={() => navigate('/')} className="p-2 hover:bg-slate-50 rounded-full transition-colors text-slate-600">
                        <ArrowLeft size={24} />
                    </button>
                    <h1 className="text-lg font-serif font-bold text-slate-800 tracking-wide">
                        MY COLLECTION
                    </h1>
                    <div className="w-10" />
                </div>
            </header>

            <main className="max-w-5xl mx-auto px-4 py-8">
                {loading ? (
                    <div className="flex justify-center py-20">
                        <div className="animate-spin text-slate-400"><Gauge size={32} /></div>
                    </div>
                ) : recipes.length === 0 ? (
                    <div className="text-center py-20">
                        <div className="inline-flex p-4 bg-slate-100 rounded-full text-slate-400 mb-4">
                            <Heart size={48} />
                        </div>
                        <h2 className="text-xl font-medium text-slate-700 mb-2">No Favorites Yet</h2>
                        <p className="text-slate-500 mb-8 max-w-xs mx-auto">Start exploring recipes and save your best culinary discoveries here.</p>
                        <button
                            onClick={() => navigate('/')}
                            className="px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium"
                        >
                            Explore Recipes
                        </button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {recipes.map((recipe, idx) => (
                            <div
                                key={recipe.recipe_id || idx}
                                onClick={() => navigate(`/recipe/${recipe.recipe_id}`, { state: { recipe } })}
                                className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all cursor-pointer group border border-slate-100"
                            >
                                <div className="aspect-[4/3] relative bg-slate-100 overflow-hidden">
                                    {recipe.cover_image ? (
                                        <img
                                            src={recipe.cover_image}
                                            alt={recipe.recipe_name}
                                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                        />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center text-slate-300">
                                            <ChefHat size={40} />
                                        </div>
                                    )}
                                    <div className="absolute top-3 right-3 bg-white/90 backdrop-blur px-2 py-1 rounded-md text-xs font-bold text-slate-700 shadow-sm uppercase tracking-wider">
                                        Saved
                                    </div>
                                </div>
                                <div className="p-5">
                                    <h3 className="text-lg font-bold text-slate-800 mb-2 font-serif">{recipe.recipe_name}</h3>
                                    <div className="flex flex-wrap gap-2 mb-4">
                                        {recipe.tags?.slice(0, 2).map(tag => (
                                            <span key={tag} className="text-xs text-slate-500 uppercase tracking-wide">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                    <div className="pt-4 border-t border-slate-50 flex items-center justify-between text-xs font-medium text-slate-400 uppercase tracking-widest">
                                        <div className="flex items-center gap-1">
                                            <Clock size={14} />
                                            <span>20 MIN</span>
                                        </div>
                                        <span>Full Recipe</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
};

export default FavoritesPage;
