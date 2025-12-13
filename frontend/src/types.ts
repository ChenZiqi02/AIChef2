export interface RecipeStep {
    // Step index for display
    step_index: number;
    description: string;
    image_url: string | null;
}

export interface Recipe {
    recipe_id: string;
    recipe_name: string;
    tags: string[];
    cover_image: string | null;
    steps: RecipeStep[];
    message: string;
    match_score?: number; // Optional, for frontend display
    cooking_time?: string; // Optional
    difficulty?: string; // Optional
}

export interface RecipeResponse {
    candidates: Recipe[]; // We will update backend to return this
    ai_message?: string;
}
