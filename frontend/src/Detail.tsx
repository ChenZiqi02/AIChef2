import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Clock, Flame, Heart, Share2, ChevronRight, ChefHat } from 'lucide-react';
import type { Recipe } from './types';
import { cn } from './lib/utils';

const RecipeDetail = () => {
    const navigate = useNavigate();
    const location = useLocation();

    // In a real app, we might fetch by ID if state is missing
    const recipe = location.state?.recipe as Recipe;

    const [isFavorite, setIsFavorite] = useState(false);

    useEffect(() => {
        window.scrollTo(0, 0);
        // Initialize isFavorite state based on localStorage
        if (recipe?.recipe_id) {
            const favIds = JSON.parse(localStorage.getItem('aichef_favorites') || '[]');
            setIsFavorite(favIds.includes(recipe.recipe_id));
        }
    }, [recipe?.recipe_id]);

    const toggleFavorite = () => {
        // 1. Manage List of IDs
        const favIds = JSON.parse(localStorage.getItem('aichef_favorites') || '[]');
        let newFavIds;

        // 2. Manage Recipe Objects Map (Data Source for Favorites Page)
        const savedRecipes = JSON.parse(localStorage.getItem('aichef_saved_recipes') || '{}');

        if (isFavorite) {
            newFavIds = favIds.filter((fid: string) => fid !== recipe.recipe_id);
            delete savedRecipes[recipe.recipe_id];
        } else {
            if (!favIds.includes(recipe.recipe_id)) {
                newFavIds = [...favIds, recipe.recipe_id];
            } else {
                newFavIds = favIds;
            }
            savedRecipes[recipe.recipe_id] = recipe;
        }

        localStorage.setItem('aichef_favorites', JSON.stringify(newFavIds));
        localStorage.setItem('aichef_saved_recipes', JSON.stringify(savedRecipes));
        setIsFavorite(!isFavorite);
    };

    if (!recipe) {
        return <div className="p-8 text-center text-red-500">Recipe not found.</div>;
    }

    return (
        <div className="min-h-screen bg-white">
            {/* Hero Image Section */}
            <div className="relative h-96 md:h-[500px]">
                <div className="absolute top-0 left-0 right-0 p-4 z-20 flex justify-between items-start">
                    <button
                        onClick={() => navigate(-1)}
                        className="p-3 bg-white/20 backdrop-blur-md hover:bg-white/30 rounded-full text-white transition-all shadow-sm"
                    >
                        <ArrowLeft size={24} />
                    </button>
                    <div className="flex gap-3">
                        <button
                            className="p-3 bg-white/20 backdrop-blur-md hover:bg-white/30 rounded-full text-white transition-all shadow-sm"
                            onClick={toggleFavorite}
                        >
                            <Heart size={24} className={cn("transition-colors duration-300", isFavorite ? "fill-red-500 text-red-500" : "text-white")} />
                        </button>
                        <button className="p-3 bg-white/20 backdrop-blur-md hover:bg-white/30 rounded-full text-white transition-all shadow-sm">
                            <Share2 size={24} />
                        </button>
                    </div>
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/30 z-10" />

                {recipe.cover_image ? (
                    <img
                        src={recipe.cover_image}
                        alt={recipe.recipe_name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                            e.currentTarget.style.display = 'none'; // Hide if broken
                        }}
                    />
                ) : (
                    <div className="w-full h-full bg-slate-200 flex items-center justify-center text-slate-400">
                        <span className="text-xl font-serif italic">No Image Available</span>
                    </div>
                )}

                <div className="absolute bottom-0 left-0 right-0 p-8 z-20 text-white"> {/* Increased padding */}
                    <div className="max-w-4xl mx-auto">
                        <h1 className="text-3xl md:text-5xl font-bold mb-3 font-serif tracking-wide">{recipe.recipe_name}</h1>
                        <div className="flex flex-wrap gap-2 text-sm md:text-base opacity-90">
                            {recipe.tags?.map(tag => (
                                <span key={tag} className="px-3 py-1 border border-white/40 rounded-full bg-black/20 backdrop-blur-md uppercase tracking-wider text-xs font-medium">{tag}</span>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Content */}
            <main className="max-w-4xl mx-auto px-6 py-12"> {/* Increased padding */}
                {/* AI Message Alert */}
                {recipe.message && (
                    <div className="mb-12 p-6 bg-orange-50/50 border border-orange-100 rounded-xl flex gap-4 items-start shadow-sm">
                        <div className="mt-1 text-orange-600 bg-orange-100 p-2 rounded-full">
                            <ChefHat size={20} />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-800 mb-2 uppercase tracking-wide text-xs">Chef's Consultant Note</h3>
                            <p className="text-slate-700 leading-relaxed font-serif text-lg italic opacity-90">{recipe.message}</p>
                        </div>
                    </div>
                )}

                <div className="grid md:grid-cols-[1fr_300px] gap-12">
                    {/* Left: Steps */}
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 mb-8 font-serif border-b pb-4">Instructions</h2>
                        <div className="space-y-12">
                            {recipe.steps.map((step, idx) => (
                                <div key={step.step_index} className="relative pl-8 border-l border-slate-200 pb-2 last:border-0 group">
                                    <div className="absolute -left-[5px] top-2 w-2.5 h-2.5 rounded-full bg-slate-300 group-hover:bg-orange-500 transition-colors" />
                                    <h3 className="text-lg font-bold text-slate-400 mb-2 flex items-center gap-2 uppercase tracking-widest text-sm">
                                        Step {step.step_index}
                                    </h3>
                                    <p className="text-slate-700 text-lg leading-relaxed mb-6 font-light">{step.description}</p>
                                    <div className="rounded-xl overflow-hidden shadow-sm aspect-video bg-slate-50 flex items-center justify-center border border-slate-100">
                                        {step.image_url ? (
                                            <img src={step.image_url} alt={`Step ${step.step_index}`} className="w-full h-full object-cover" />
                                        ) : (
                                            <div className="flex flex-col items-center justify-center text-slate-300">
                                                <ChefHat size={32} className="mb-2 opacity-50" />
                                                <span className="text-xs font-medium uppercase tracking-wider">Cooking...</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Right: Info (Sticky) */}
                    <div className="space-y-6">
                        <div className="bg-slate-50 p-8 rounded-2xl sticky top-24 border border-slate-100">
                            <h3 className="font-bold text-slate-800 mb-6 font-serif text-xl border-b border-slate-200 pb-2">Recipe Info</h3>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between py-2 border-b border-slate-200 border-dashed">
                                    <div className="flex items-center gap-2 text-slate-500 uppercase text-xs tracking-wider">
                                        <Clock size={16} />
                                        <span>Prep Time</span>
                                    </div>
                                    <span className="font-medium text-slate-900 font-serif">10 mins</span>
                                </div>
                                <div className="flex items-center justify-between py-2 border-b border-slate-200 border-dashed">
                                    <div className="flex items-center gap-2 text-slate-500 uppercase text-xs tracking-wider">
                                        <Flame size={16} />
                                        <span>Cook Time</span>
                                    </div>
                                    <span className="font-medium text-slate-900 font-serif">20 mins</span>
                                </div>
                                {/* Removed Start Cooking Mode Button */}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default RecipeDetail;
