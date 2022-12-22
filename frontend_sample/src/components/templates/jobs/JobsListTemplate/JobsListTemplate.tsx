import { useGetJobs } from "lib/hooks/api/jobs";
import { FC } from "react";


const JobsListTemplate: FC = () => {
    const {data: jobsResponse} = useGetJobs({q: "", page:1, perPage:20})

    return (     <div>
        {jobsResponse?.data?.map((d) => {
            return (<div key={d.id}>{d.title}</div>)
        })}
     </div>)
}

export default JobsListTemplate
