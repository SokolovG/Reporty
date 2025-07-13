import type {User} from '../types/user'
import apiClient from "$lib/api/client";
export async function loginUser(user: User){
    try{
        console.log(user)
        const response = await apiClient.post('/login', user);
        return response.data;
    } catch (error) {
        console.log(error);
        throw new Error("Error during login");
    }
}
