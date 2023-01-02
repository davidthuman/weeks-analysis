import PocketBase from "pocketbase";
import { env } from '../../../env/server.mjs'
import getAuth from "../get-auth";

import type { NextApiRequest, NextApiResponse } from "next"; 

export default async function handler(req: NextApiRequest, res: NextApiResponse) {

    const pb = new PocketBase('http://0.0.0.0:8090/');
    const dataAuth = await pb.admins.authWithPassword(env.NEXT_PUBLIC_POCKETBASE_EMAIL, env.NEXT_PUBLIC_POCKETBASE_PASSWORD)

    const pb_1 = await getAuth();
    const days = await pb.collection('days').getFullList();
    res.status(200).json(days)


}





