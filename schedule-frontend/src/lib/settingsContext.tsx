import {createContext, useContext, useState} from 'react';

const defaultSettingsState = {
    group: null
}

const SettingsContext = createContext({
    state: defaultSettingsState,
});

const LOCAL_STORAGE_KEY = 'settings';

const getStateFromLocalStorage = () => {
    const data = localStorage.getItem(LOCAL_STORAGE_KEY);
    return data ? JSON.parse(data) : defaultSettingsState;
}

export const SettingsContextProvider = ({children}) => {
    const [settingsState, setInternalSettingsState] = useState(getStateFromLocalStorage());
    const setSettingsState = (newState) => {
        setInternalSettingsState(newState);
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(newState));
    }
    return (
        <SettingsContext.Provider value={{
            settingsState,
            setSettingsState
        }}>
            {children}
        </SettingsContext.Provider>
    )
}

export const useSettings = () => useContext(SettingsContext);

