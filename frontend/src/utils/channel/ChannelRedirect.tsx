import { Suspense, useEffect } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { hasChatlyUserRole } from '../roles'
import { FullPageLoader } from '@/components/layout/Loaders'
import AddChatlyUsersPage from '@/pages/AddChatlyUsersPage'
import { UserListProvider } from '../users/UserListProvider'
import { ChannelListProvider } from './ChannelListProvider'

/**
 * Redirects to the last channel visited by the user
 * If last channel is not found, redirects to general channel
 */
export const ChannelRedirect = () => {

    const lastChannel = localStorage.getItem('chatlyLastChannel') ?? 'general'

    const navigate = useNavigate()
    const { pathname } = useLocation()

    const isChatlyUser = hasChatlyUserRole()

    useEffect(() => {
        // If on desktop, redirect to last channel
        // If on mobile, redirect to channel list
        const isDesktop = window.matchMedia('(min-width: 768px)').matches
        const path = isDesktop ? `/channel/${lastChannel}` : '/channel'
        if (isChatlyUser && (pathname === '/channel' || pathname === '/')) navigate(path, {
            replace: true
        })
    }, [pathname, isChatlyUser])

    if (isChatlyUser) {
        return (
            <UserListProvider>
                <ChannelListProvider>
                    <Outlet />
                </ChannelListProvider>
            </UserListProvider>
        )

    }
    return <Suspense fallback={<FullPageLoader />}>
        <AddChatlyUsersPage />
    </Suspense>
}