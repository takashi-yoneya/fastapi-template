import JobsListTemplate from "components/templates/jobs/JobsListTemplate/JobsListTemplate"
import { useGetJobs } from "lib/hooks/api/jobs"
import { NextPage } from "next"

const JobsPage: NextPage = () => {

 return (
    <>
        <JobsListTemplate />
    </>
 )
}

export default JobsPage
