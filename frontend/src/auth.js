import axios from 'axios';

export async function isAuthenticated() {
    try {
        const apiUrl = process.env.VUE_APP_API_BASE_URL;
        const path = `${apiUrl}/is-authenticated`;

        const response = await axios.get(path, {withCredentials: true});

        return response.data.isLogged;

    } catch (error) {
        console.error(error);
        return false;
    }
}
