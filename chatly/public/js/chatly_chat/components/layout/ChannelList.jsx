import React from 'react'
import useChannelList from '../../hooks/useChannelList'
import useGetUser from '../../hooks/useGetUser'
import Avatar from '../common/Avatar'
import ChannelIcon from '../common/ChannelIcon'
import { useChannelUnreadCount } from '../../hooks/useUnreadCount'

const ChannelList = ({ onSelectChannel }) => {

    const { isLoading, channels, dm_channels } = useChannelList()

    return (
        <div className="chatly-channel-list">
            {isLoading && <SkeletonLoader />}
            <h4>Channels</h4>
            {channels?.map(channel => <ChannelListItem key={channel.name} channel={channel} onClick={() => onSelectChannel(channel.name)} />)}
            <h4 style={{ paddingTop: '1rem' }}>Direct Messages</h4>
            {dm_channels?.map(channel => <DMChannelListItem key={channel.name} channel={channel} onClick={() => onSelectChannel(channel.name)} />)}
        </div>
    )
}

export default ChannelList


const SkeletonLoader = () => {

    return <>{Array.from({ length: 17 }).map((_, i) => <div key={i} className="chatly-channel-list-item">
        <span className='skeleton'></span>
    </div>)}
    </>

}

const ChannelListItem = ({ channel, onClick }) => {

    const count = useChannelUnreadCount(channel.name)
    return <button className="chatly-channel-list-item" onClick={onClick}>
        <div className='channel-label'>
            <span className='chatly-channel-icon'>
                <ChannelIcon channelType={channel.channel_type} />
            </span>
            <span className="chatly-channel-list-item__name">{channel.channel_name}</span>
        </div>
        <div>
            {count ? <span className="channel-unread-count">{count}</span> : null}
        </div>
    </button>
}

const DMChannelListItem = ({ channel, onClick }) => {

    const user = useGetUser(channel.peer_user_id)

    const count = useChannelUnreadCount(channel.name)

    return <button className="chatly-channel-list-item" onClick={onClick}>
        <div className='channel-label'>
            <Avatar user={user} />
            <span className="chatly-channel-list-item__name">{user?.full_name}</span>
        </div>
        <div>
            {count ? <span className="channel-unread-count">{count}</span> : null}
        </div>
    </button>
}