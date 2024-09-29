import InfoDialog from "./InfoDialog.tsx";
import {useSettings} from "@/lib/settingsContext.tsx";

const Navbar = () => {
    const {settingsState} = useSettings()
    return (
        <nav className="h-full">
            <div className="flex items-center justify-between px-2 py-4">

                <div className="flex items-center">
                    <span className="font-bold">
                    Plan zajęć ZP-WNOZ
                </span>
                    <span className="mx-5">
                    Twoja grupa {settingsState.group}
                </span>
                    <InfoDialog/>
                </div>
                <div>
                    <a href="https://github.com/micorix/wnoz-schedule" target="_blank" rel="noreferrer" className="text-black underline">
                        GitHub
                    </a>
                </div>
            </div>
        </nav>
    )
}

export default Navbar;