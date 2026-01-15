export const getNamespacedKey = (key: string, username: string) => {
    return `${key}_${username}`;
};
