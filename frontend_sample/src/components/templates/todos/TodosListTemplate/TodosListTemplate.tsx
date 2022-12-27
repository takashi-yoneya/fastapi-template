import { useGetTodos } from "lib/hooks/api/todos";
import { useRouter } from "next/router";
import { FC, useState } from "react";

const TodosListTemplate: FC = () => {
  const router = useRouter();
  const [page, setPage] = useState<number>(1);
  const [perPage, setPerPage] = useState<number>(5);
  const [keyword, setKeyword] = useState<string>("");
  const { data: todosResponse } = useGetTodos({
    q: keyword,
    page: page,
    perPage: perPage,
  });

  return (
    <div>
      <h2>Todo List</h2>
      <div>
        <button onClick={() => router.push("/todos/create")}>新規作成</button>
      </div>

      <div>
        <div>
          keyword:{" "}
          <input
            value={keyword}
            onChange={(e) => {
              setKeyword(e.target.value);
            }}
          />
        </div>
        <div>
          perPage:{" "}
          <input
            value={perPage}
            onChange={(e) => {
              setPerPage(e.target.value as unknown as number);
            }}
          />
        </div>
      </div>
      <button
        onClick={() => {
          page > 1 && setPage(page - 1);
        }}
      >
        previous page
      </button>
      <button
        onClick={() => {
          console.log(todosResponse?.meta?.totalPageCount, page);
          todosResponse?.meta?.totalPageCount &&
            todosResponse?.meta?.totalPageCount > page &&
            setPage(page + 1);
        }}
      >
        next page
      </button>
      <div>
        page: {todosResponse?.meta?.currentPage}/
        {todosResponse?.meta?.totalPageCount}
      </div>
      <div>total count: {todosResponse?.meta?.totalDataCount}</div>
      <hr></hr>
      {todosResponse?.data?.map((d, i) => {
        return (
          <div key={d.id}>
            <div>
              {i + 1}:{d.title}
            </div>
            <div>
              {d.tags?.map((tag) => {
                return <div key={d.id}>{tag.name}</div>;
              })}
            </div>
            <div>
              <button onClick={() => router.push(`/todos/edit/?id=${d.id}`)}>
                編集
              </button>
            </div>
            <hr></hr>
          </div>
        );
      })}
    </div>
  );
};

export default TodosListTemplate;
