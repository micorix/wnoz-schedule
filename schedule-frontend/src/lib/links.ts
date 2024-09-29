const ARTIFACTS_BASE_URL = `https://raw.githubusercontent.com/micorix/wnoz-schedule/refs/heads/master/artifacts`

export const INFO_URL = `${ARTIFACTS_BASE_URL}/2024-licencjackie-stacjonarne/info.json`

export const getGroupActivitiesUrl = (groupId: string) => `${ARTIFACTS_BASE_URL}/2024-licencjackie-stacjonarne/${groupId}/activities.json`
export const getGroupICalUrl = (groupId: string) => `${ARTIFACTS_BASE_URL}/2024-licencjackie-stacjonarne/${groupId}/calendar.ics`