import React, { createContext, useContext, useState } from 'react';

interface UserContextType {
    username: string;
    switchUser: (name: string) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    // 默认从 localStorage 读取，如果没有则为 "default"
    const [username, setUsername] = useState(() => {
        return localStorage.getItem('aichef_username') || 'default';
    });

    const switchUser = (name: string) => {
        const newName = name.trim() || 'default';
        setUsername(newName);
        localStorage.setItem('aichef_username', newName);
        // 简单暴力：切换用户后刷新页面，确保所有数据 (如缓存) 清空或重新加载
        window.location.reload();
    };

    return (
        <UserContext.Provider value={{ username, switchUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
};
