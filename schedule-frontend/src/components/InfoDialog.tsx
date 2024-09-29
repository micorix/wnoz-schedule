import {Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger} from "./ui/dialog.tsx";
import {AlertCircle} from "lucide-react";
import {Alert, AlertDescription, AlertTitle} from "../../@/components/ui/alert.tsx";
import {Select} from "@/components/ui/select.tsx";
import {SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select.tsx";
import {useSettings} from "@/lib/settingsContext.tsx";
import {useQuery} from "@tanstack/react-query";
import {getGroupICalUrl, INFO_URL} from "@/lib/links.ts";
import {useEffect, useState} from "react";
import dayjs from "dayjs";

const LOCAL_STORAGE_KEY = 'visited'

const isFirstTimeVisit = () => {
    return localStorage.getItem(LOCAL_STORAGE_KEY) !== 'true'
}

const setVisited = () => {
    localStorage.setItem(LOCAL_STORAGE_KEY, 'true')
}

const getInfo = async () => {
    return fetch(INFO_URL).then((response) => response.json())
}

const InfoDialog = () => {
    const [copied, setCopied] = useState(false)
    const {settingsState, setSettingsState} = useSettings()
    const {data, isLoading} = useQuery({
        queryKey: ['info'],
        queryFn: getInfo,
        placeholderData: {
            group_names: [],
            downloaded_at: null
        }
    })

    useEffect(() => {
        setVisited()
    }, []);

    const iCalUrl = settingsState.group ? getGroupICalUrl(settingsState.group) : ''

    const onChangeGroup = (group) => {
        setSettingsState({...settingsState, group})
    }

    const handleInputClick = async (e) => {
        const value = e.target.value
        e.target.select()
        await navigator.clipboard.writeText(value)
        setCopied(true)
        setTimeout(() => {
            setCopied(false)
        }, 2000)
    }

    return (
        <Dialog defaultOpen={isFirstTimeVisit()}>
            <DialogTrigger className="rounded border px-3 py-1 border border-black text-black">Opcje &
                info</DialogTrigger>
            <DialogContent className="max-w-3xl">
                <DialogHeader>
                    <DialogTitle className="text-3xl text-center">Nieoficjalna aplikacja <br/>planu zajęć dla
                        kierunku
                        zdrowie publiczne
                    </DialogTitle>
                    <DialogDescription>
                        <div className="flex items-center justify-center py-2 mt-2 mb-5 bg-red-50 rounded-xl">
                            <AlertCircle className="w-6 h-6 mr-2 text-red-500"/>
                            <span className="">Plan zajęć jest dostępny tylko dla pierwszego roku 2024</span>
                        </div>
                        <div className="">
                            <h2 className="text-xl font-semibold">Jak korzystać?</h2>
                            <p className="text-sm">
                                Plan aktualizuje się codziennie o czwartej rano na podstawie plików Excel
                                udostępnionych
                                na
                                {' '}
                                <a href="https://wnoz.wum.edu.pl/pl/zdrowie-publiczne-plan-zajec"
                                   className="underline">stronie
                                    WNOZ</a>.
                                <br />
                                <br/>
                                <strong className="underline">I did my best, ale NIE gwarantuję poprawnego działania
                                    programu lub terminowego naprawiania usterek</strong>
                            </p>
                            <h3 className="mt-5 text-lg font-semibold">Google/Outlook calendar</h3>
                            <p className="text-sm">
                                Dostępny jest także stały link do kalendarza w formacie iCal, który można dodać do
                                Google Kalendarza (opóźnienie w synchronizacji do 24h).
                            </p>
                        </div>
                        <hr className="my-5"/>
                        <div className="flex items-center justify-center">
                            <span className="mr-5">Wybierz swoją grupę</span>
                            <div>
                                {
                                    isLoading ? (
                                        <span className="italic">Ładowanie...</span>
                                    ) : (
                                        <Select value={settingsState.group} onValueChange={onChangeGroup}>
                                            <SelectTrigger>
                                                <SelectValue>{settingsState.group || 'Twoja grupa'}</SelectValue>
                                            </SelectTrigger>
                                            <SelectContent>
                                                {
                                                    data.group_names.map((group) => (
                                                        <SelectItem key={group} value={group}>{group}</SelectItem>
                                                    ))
                                                }
                                            </SelectContent>
                                        </Select>
                                    )
                                }
                            </div>
                        </div>
                        <hr className="my-5"/>
                        {
                            settingsState.group && (
                                <div className="">
                                    <p>
                                        Adres kalendarza w formacie iCal dla grupy {settingsState.group}:
                                    </p>
                                    <input onClick={handleInputClick} type="text" value={iCalUrl} readOnly
                                           className="mt-1 w-full border border-black rounded p-1"/>
                                    <div className="h-7">
                                        {copied && (
                                            <small className="text-gray-500">Skopiowano do schowka</small>
                                        )}
                                    </div>
                                    <p className="">
                                        Ostatnia aktualizacja względem pliku
                                        Excel: {data.downloaded_at ? dayjs(data.downloaded_at).format('DD.MM.YYYY HH:mm') : 'N/A'}
                                    </p>

                                </div>
                            )
                        }
                        <p className="font-mono mt-2 text-small text-gray-400">
                            Apikacja udostępniona jest na licencji MIT.
                            <br />
                            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
                                KIND
                        </p>
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    )
        ;
}
export default InfoDialog;