import {Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger} from "./ui/dialog.tsx";
import {AlertCircle} from "lucide-react";
import {Alert, AlertDescription, AlertTitle} from "../../@/components/ui/alert.tsx";
import {Select} from "@/components/ui/select.tsx";
import {SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select.tsx";
import dayjs from "dayjs";

const WEEKDAYS = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota'];

const EventDialog = ({event, onClose}) => {
    const handleOpenChange = (open) => {
        if (!open) onClose()
    }
    return (
        <Dialog open={true} onOpenChange={handleOpenChange}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>
                        <div className="flex  items-center">
                            <span style={{background: event.color}} className="w-4 h-4 rounded-full block"></span>
                            <span className="ml-2">{event.title}</span>
                        </div>
                    </DialogTitle>
                    <DialogDescription>
                        <div className="">
                            <ul className="mt-2 text-base list-disc list-inside">
                                <li>Data: <span className="font-bold">
                                    <span className="text-black">
                                        {dayjs(event.start).format('DD.MM.YYYY')}
                                    </span>
                                    {' '}
                                    ({WEEKDAYS[event.start.getDay()].toLowerCase()})
                                </span>
                                </li>
                                <li>Godzina:
                                    {' '}
                                    <span className="text-black font-bold">
                                        {dayjs(event.start).format('HH:mm')} - {dayjs(event.end).format('HH:mm')}
                                    </span>
                                    {' '}
                                    <span className="font-bold">
                                        ({dayjs(event.end).diff(dayjs(event.start), 'hour', true)}h)
                                    </span>
                                </li>
                            </ul>
                            <hr className="my-2"/>
                            <p className="mt-2 text-base">
                                {event.description}
                            </p>
                        </div>
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    );
}
export default EventDialog;