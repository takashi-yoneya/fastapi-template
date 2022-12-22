import JobsListTemplate from "components/templates/jobs/JobsListTemplate/JobsListTemplate"
import JobsUpdateTemplate from "components/templates/jobs/JobUpdateTemplate/JobsUpdateTemplate"
import { useGetJobs } from "lib/hooks/api/jobs"
import { NextPage } from "next"

const JobsUpdatePage: NextPage = () => {

 return (
    <>
        <JobsUpdateTemplate />
    </>
 )
}

export default JobsUpdatePage
