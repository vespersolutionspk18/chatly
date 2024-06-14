import { ChatlyUser } from '@/types/Chatly/ChatlyUser'
import { useFrappeGetCall } from 'frappe-react-sdk'

const useCurrentChatlyUser = () => {

    const { data, mutate } = useFrappeGetCall<{ message: ChatlyUser }>('chatly.api.chatly_users.get_current_chatly_user',
        undefined,
        'my_profile',
        {
            // revalidateIfStale: false,
            revalidateOnFocus: false,
            shouldRetryOnError: false,
            revalidateOnReconnect: true
        }
    )

    return {
        myProfile: data?.message,
        mutate
    }

}

export default useCurrentChatlyUser