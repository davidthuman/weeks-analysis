import { type NextPage } from "next";

import Login from "../../components/login-btn";

import PocketBase from "pocketbase";
import { env  } from "../../env/client.mjs"

import LevelTabs from "./levelTabs";


export async function getStaticProps() {
    const pb = new PocketBase('http://0.0.0.0:8090/');

    const dataAuth = await pb.admins.authWithPassword(env.NEXT_PUBLIC_POCKETBASE_EMAIL, env.NEXT_PUBLIC_POCKETBASE_PASSWORD)
    const l1_records = await pb.collection('level_one').getFullList();
    const l2_records = await pb.collection('level_two').getFullList();
    const l3_records = await pb.collection('level_three').getFullList();
    const level_one = JSON.parse(JSON.stringify(l1_records))
    const level_two = JSON.parse(JSON.stringify(l2_records))
    const level_three = JSON.parse(JSON.stringify(l3_records))
    return { props: { level_one, level_two, level_three } }

}

export default function Admin( props : any) {


    
    const action: string = "Working"
  
    return (
        <div className="flex flex-col justify-items-center items-center">
            <h1 className="bg-[#b167c0] text-center text-5xl text-white font-extrabold tracking-tight h-20 w-full">Admin Panel</h1>
            <div>
                <div>Categorize</div>
            </div>
            <div className="flex flex-row">
                <div className="flex flex-col">
                    <div className="text-2xl">
                        Action: {action}
                    </div>
                    <LevelTabs level_one={props.level_one} level_two={props.level_two} level_three={props.level_three} />
                </div>
            </div>
        </div>
    )
}





