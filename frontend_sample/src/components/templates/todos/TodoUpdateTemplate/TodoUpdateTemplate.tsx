import { TodoUpdate } from "api_clients";
import { useGetTodoById, useUpdateTodo } from "lib/hooks/api/todos";
import { useRouter } from "next/router";
import { FC, useCallback, useEffect, useState } from "react";

const TodoUpdateTemplate: FC = () => {
  const [requestData, setRequestData] = useState<TodoUpdate>();
  const [id, setId] = useState<string>("");
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  const router = useRouter();
  const { data: todoResponse } = useGetTodoById(router.query.id as string);
  const { mutateAsync: updateMutateAsync, isLoading: isLoading } =
    useUpdateTodo(id);

  const handleChangeValue = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
      const { name, value } = e.target;
      setRequestData({
        ...requestData,
        [name]: value,
      });
    },
    [setRequestData, requestData],
  );

  useEffect(() => {
    setId(router.query.id as string);
  }, [router.query.id]);

  useEffect(() => {
    if (!todoResponse) return;
    setRequestData(todoResponse);
  }, [todoResponse]);

  const handleClickUpdateButton = async (): Promise<void> => {
    if (!requestData) return;
    await updateMutateAsync(
      requestData,
      (responseData) => {
        setIsSuccess(true);
        console.log("success.", responseData);
      },
      (error) => {
        setIsSuccess(false);
        console.log("error.", error);
      },
    );
  };
  return (
    <div>
      <h2>Todo Edit</h2>
      <div>id:{id}</div>
      <div>
        タイトル:
        <input
          name="title"
          value={requestData?.title}
          onChange={handleChangeValue}
        />
      </div>
      <div>
        説明:
        <textarea
          name="description"
          value={requestData?.description}
          onChange={handleChangeValue}
        />
      </div>
      <button onClick={() => router.back()}>キャンセル</button>
      <button onClick={handleClickUpdateButton}>更新</button>
      <div>{isLoading && "処理中"}</div>
      <div>{!isLoading && isSuccess && "完了"}</div>
    </div>
  );
};

export default TodoUpdateTemplate;
