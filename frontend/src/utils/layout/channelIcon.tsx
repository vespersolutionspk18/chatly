import { BiGlobe, BiHash, BiLockAlt } from 'react-icons/bi';
import { ChatlyChannel } from "../../../../types/ChatlyChannelManagement/ChatlyChannel";
import { IconBaseProps } from 'react-icons';

export const getChannelIcon = (type: ChatlyChannel['type']) => {

    switch (type) {
        case 'Private': return BiLockAlt
        case 'Open': return BiGlobe
        default: return BiHash
    }
}

interface ChannelIconProps extends IconBaseProps {
    type: ChatlyChannel['type']
}

export const ChannelIcon = ({ type, ...props }: ChannelIconProps) => {

    if (!type) return null

    if (type === 'Private') return <BiLockAlt {...props} />
    if (type === 'Open') return <BiGlobe {...props} />
    return <BiHash {...props} />

}
