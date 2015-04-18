from exception import themis_exception;
from exception import THEMIS_CODES;
from ctypes import *
themis = cdll.LoadLibrary('libthemis.so')

class smessage(object):
    def __init__(self, private_key_, peer_public_key_):
	self.private_key=private_key_;
        self.peer_public_key=peer_public_key_;

    def wrap(self, message):
	encrypted_message_length=c_int(0);
	res=themis.themis_secure_message_wrap(self.private_key ,len(self.private_key), self.peer_public_key, len(self.peer_public_key), message, len(message), None, byref(encrypted_message_length));
        if res!=THEMIS_CODES.BUFFER_TOO_SMALL:
	    raise themis_exception(res,"themis_secure_message_wrap (wrapped message length determination) error");
	encrypted_message=create_string_buffer(encrypted_message_length.value);
	res=themis.themis_secure_message_wrap(self.private_key ,len(self.private_key), self.peer_public_key, len(self.peer_public_key), message, len(message), encrypted_message, byref(encrypted_message_length));
        if res!=THEMIS_CODES.SUCCESS:
	    raise themis_exception(res, "themis_secure_message_wrap error");
        return string_at(encrypted_message, encrypted_message_length.value);

    def unwrap(self,message):
        plain_message_length=c_int(0);
	res=themis.themis_secure_message_unwrap(self.private_key, len(self.private_key), self.peer_public_key ,len(self.peer_public_key), message, len(message), None, byref(plain_message_length));
        if res!=THEMIS_CODES.BUFFER_TOO_SMALL:
	    raise themis_exception(res, "themis_secure_message_unwrap (plain message length determination) error");
	plain_message=create_string_buffer(plain_message_length.value);
	res=themis.themis_secure_message_unwrap(self.private_key, len(self.private_key), self.peer_public_key ,len(self.peer_public_key), message, len(message), plain_message, byref(plain_message_length));
        if res!=THEMIS_CODES.SUCCES:
            raise themis_exception(res,"themis_secure_message_unwrap decrypting error");
	return string_at(plain_message, plain_message_length.value);

