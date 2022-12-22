import { JobUpdate } from "api_clients";
import {  useGetJobById, useUpdateJob } from "lib/hooks/api/jobs";
import { useRouter } from "next/router";
import { FC, useCallback, useEffect, useState } from "react";


const JobUpdateTemplate: FC = () => {
    const [requestData, setRequestData] = useState<JobUpdate>()
    const [id, setId] = useState<string>("")
    const router = useRouter()
    const {data: jobResponse} = useGetJobById(router.query.id as string)
    const { mutateAsync: updateMutateAsync, isLoading: isLoading } = useUpdateJob(id);

    const handleChangeValue = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
        const { name, value } = e.target;
        setRequestData({
          ...requestData,
          [name]: value,
        });
    },[setRequestData, requestData])

    useEffect( () => {
      setId(router.query.id as string)
    }, [router.query.id])

    useEffect( () => {
      if (!jobResponse) return
      setRequestData(jobResponse)
      console.log(requestData, jobResponse)
    }, [jobResponse])

    const handleClickUpdateButton = async (): Promise<void> => {
        if (!requestData) return
        await updateMutateAsync(
          requestData,
          (responseData) => {
            console.log('success.', responseData);
          },
          (error) => {
            console.log('error.', error);
          },
        );
      };
    return (
      <div>
        タイトル:<input name="title"  value={requestData?.title} onChange={handleChangeValue}/>
        <button onClick={handleClickUpdateButton}>更新</button>
     </div>
    )
}

export default JobUpdateTemplate
