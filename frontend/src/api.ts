export const apiUrl= import.meta.env.VITE_API_URL

export interface Message{
    username: string;
    content:string;
    id?:Number | null ;
}


export async function addMessage(msg: Message){
    const response = await fetch(`${apiUrl}/addMessage`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(msg),
    })
    console.log(response);
    return response.json()
}

export async function getMessages(username: string): Promise<Message[]>{
    const response = await fetch(`${apiUrl}/getMessages?username=${encodeURIComponent(username)}`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        }
    })
    console.log(response);
    return response.json()
}

export async function addToFavoritesBack(username:string, msg: Message){
    const response = await fetch(`${apiUrl}/addToFavorites`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({username: username, id: msg.id}),
    })
    return response.json()
}

export async function getFavorites(username: string): Promise<Activity[]>{
    const response = await fetch(`${apiUrl}/getFavorites?username=${encodeURIComponent(username)}`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        }
    })
    return response.json()
}

export async function removeFromFavoritesBack(username: string, act:Activity) {
    const response = await fetch(`${apiUrl}/removeFavorite`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        username: username, id:act.id}),
    });
    return response.json() as Promise<Activity[]>;
  }

export interface Activity{
    name: string;
    short_description: string;
    long_description: string;
    id:number;
}


  export interface ActivityDetail {
    time: string;
    name: string;
    duration: string;
    end_time: string;
    description: string;
    explanations?: string | null;
}

export interface DayDetail {
    day: number;
    activities: ActivityDetail[];
}

export interface Schedule {
    title: string;
    days: DayDetail[];
    explanations: string;
}