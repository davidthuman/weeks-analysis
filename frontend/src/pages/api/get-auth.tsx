import PocketBase from "pocketbase";
import { env } from "../../env/server.mjs";


export default async function getAuth() {

    const pb = new PocketBase('http://127.0.0.1:8090/');
    const authData = await pb.admins.authWithPassword(env.NEXT_PUBLIC_POCKETBASE_EMAIL, env.NEXT_PUBLIC_POCKETBASE_PASSWORD)
    return pb;
}