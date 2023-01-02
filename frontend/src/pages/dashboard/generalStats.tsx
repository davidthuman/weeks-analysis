import useSwr from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export default function GeneralStats(props: any) {

    const { data, error } = useSwr('api/dashboard/generalStats', fetcher)
    if (error) return <div>Failed to load data</div>
    if (!data) return <div>Loading ...</div>

    return (
        <div>
            Total Actions: {data.length}
        </div>
    )
}
