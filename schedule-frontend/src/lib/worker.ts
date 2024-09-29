import {QueryClient} from "@tanstack/react-query";
import {getGroupActivitiesUrl} from "@/lib/links.ts";


const mapActivity = (activity) => {
    return {
        start: new Date(activity.start_date),
        end: new Date(activity.end_date),
        title: activity.title,
        description: 'aaa',
        color: 'blue'
    }
}
const getEvents = async (groupId) => {
    const response = await fetch(getGroupActivitiesUrl(groupId));
    const data = await response.json();
    return data.map(mapActivity);
}

const queryClient = new QueryClient()


self.addEventListener('message', async (event) => {
    switch (event.data.type) {
        case 'getEvents':
            const {groupId, range} = event.data.payload;
            const events = await queryClient.fetchQuery({
                queryKey: ['events', groupId],
                queryFn: () => getEvents(groupId),
                placeholderData: []
            })
            const filteredEvents = events.filter((event) => event.start >= range.start && event.end <= range.end);
            self.postMessage({type: 'done', events: filteredEvents});
            break;
    }

})