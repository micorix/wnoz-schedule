import * as React from 'react';
import './App.css';
import {Calendar, dayjsLocalizer} from "react-big-calendar";
import dayjs from "dayjs";
import timezone from 'dayjs/plugin/timezone'
import EventWorker from './lib/worker.ts?worker'

dayjs.extend(timezone)
import 'react-big-calendar/lib/css/react-big-calendar.css';

import Navbar from "./components/Navbar.tsx";
import {useQuery} from "@tanstack/react-query";
import EventDialog from "@/components/EventDialog.tsx";
import {useEffect} from "react";
import {useSettings} from "@/lib/settingsContext.tsx";

const localizer = dayjsLocalizer(dayjs);

const getDefaultRange = () => {
    const now = new Date();

    // Start of the current month
    const start = new Date(now.getFullYear(), now.getMonth(), 1);

    // End of the current month + 7
    const end = new Date(now.getFullYear(), now.getMonth() + 1, 7);

    return {
        start: start,
        end: end
    };
}

const worker = new EventWorker()
const DAY = 60 * 60 * 24 * 1000;


function App() {
    const [range, setRange] = React.useState(getDefaultRange())
    const [events, setEvents] = React.useState([])
    const [isLoading, setIsLoading] = React.useState(true);
    const {settingsState} = useSettings()

    useEffect(() => {
        const abortController = new AbortController();

        worker.addEventListener('message', e => {
            if (e.data.type === 'done') {
                setEvents(e.data.events)
                setIsLoading(false)
            }
        }, {signal: abortController.signal});

        return () => {
            setIsLoading(false);
            abortController.abort()
        }
    }, [])

    useEffect(() => {
        setIsLoading(true);
        let rangeToSend = range;
        if(Array.isArray(rangeToSend)) {
            if(rangeToSend.length === 1) {
                rangeToSend = {
                    start: rangeToSend[0],
                    end: new Date(rangeToSend[0].getTime() + DAY)
                }
            } else {
                rangeToSend = {
                    start: rangeToSend[0],
                    end: rangeToSend[rangeToSend.length-1]
                }
            }
        }
        if(settingsState.group)
        worker.postMessage({
            type: 'getEvents',
            payload: {
                groupId: settingsState.group,
                range: rangeToSend
            }
        });
    }, [range, settingsState.group]);
    const [selectedEvent, setSelectedEvent] = React.useState(null);

    return (
        <div className="h-full">
               {
                    isLoading && (
                        <div className="absolute bottom-0 left-0 w-full z-30 bg-black text-white text-center py-0.5 px-1">
                            <span>Ładowanie...</span>
                        </div>
                    )
                }
            <div className="h-20 w-full bg-white">
                <Navbar/>
            </div>
            {
                selectedEvent && (
                    <EventDialog event={selectedEvent} onClose={() => setSelectedEvent(null)}/>
                )
            }

            <div className="w-full h-[calc(100vh-5rem)]">

                <Calendar
                    localizer={localizer}
                    showMultiDayTimes
                    step={60}
                    events={events}
                    onSelectEvent={event => setSelectedEvent(event)}
                    onRangeChange={(newRange) => setRange(newRange)}
                    popup={true}
                    defaultView="agenda"
                    components={{
                        event: ({event}) => (
                            <div className="relative px-1 py-0.5 cursor-pointer" style={{background: 'transparent'}}>
                                <div style={{background: event.color}}
                                     className="absolute top-0 left-0 w-full h-full rounded-lg opacity-20 z-10"/>
                                <span className="relative text-black/80 z-20 ">
                                    {event.title}
                                </span>
                            </div>
                        )
                    }}
                />
            </div>
        </div>
    );
}

export default App;