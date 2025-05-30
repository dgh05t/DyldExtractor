"""Structs for dyld

This is mainly sourced from
https://opensource.apple.com/source/dyld/dyld-832.7.3/dyld3/shared-cache/dyld_cache_format.h.auto.html
"""

import sys
from ctypes import (
	c_char,
	c_uint8,
	c_uint32,
	c_uint64,
	Union,
	sizeof
)

from DyldExtractor.structure import Structure


class dyld_cache_header(Structure):
	magic: bytes 					# e.g. "dyld_v0    i386"
	mappingOffset: int 				# file offset to first dyld_cache_mapping_info
	mappingCount: int 				# number of dyld_cache_mapping_info entries
	imagesOffsetOld: int 			# UNUSED: moved to imagesOffset to prevent older dsc_extractors from crashing
	imagesCountOld: int 			# UNUSED: moved to imagesCount to prevent older dsc_extractors from crashing
	dyldBaseAddress: int 			# base address of dyld when cache was built
	codeSignatureOffset: int 		# file offset of code signature blob
	codeSignatureSize: int 			# size of code signature blob (zero means to end of file)
	slideInfoOffsetUnused: int 		# unused.  Used to be file offset of kernel slid info
	slideInfoSizeUnused: int 		# unused.  Used to be size of kernel slid info
	localSymbolsOffset: int 		# file offset of where local symbols are stored
	localSymbolsSize: int 			# size of local symbols information
	uuid: bytes 					# unique value for each shared cache file
	cacheType: int 					# 0 for development, 1 for production, 2 for multi-cache
	branchPoolsOffset: int 			# file offset to table of uint64_t pool addresses
	branchPoolsCount: int 			# number of uint64_t entries
	dyldInCacheMH: int 				# (unslid) address of mach_header of dyld in cache
	dyldInCacheEntry: int 			# (unslid) address of entry point (_dyld_start) of dyld in cache
	imagesTextOffset: int 			# file offset to first dyld_cache_image_text_info
	imagesTextCount: int 			# number of dyld_cache_image_text_info entries
	patchInfoAddr: int 				# (unslid) address of dyld_cache_patch_info
	patchInfoSize: int 				# Size of all of the patch information pointed to via the dyld_cache_patch_info
	otherImageGroupAddrUnused: int 	# unused
	otherImageGroupSizeUnused: int 	# unused
	progClosuresAddr: int 			# (unslid) address of list of program launch closures
	progClosuresSize: int 			# size of list of program launch closures
	progClosuresTrieAddr: int 		# (unslid) address of trie of indexes into program launch closures
	progClosuresTrieSize: int 		# size of trie of indexes into program launch closures
	platform: int 					# platform number (macOS=1, etc)
	formatVersion: int 				# dyld3::closure::kFormatVersion
	dylibsExpectedOnDisk: int 		# dyld should expect the dylib exists on disk and to compare inode/mtime to see if cache is valid
	simulator: int 					# for simulator of specified platform
	locallyBuiltCache: int 			# 0 for B&I built cache, 1 for locally built cache
	builtFromChainedFixups: int 	# some dylib in cache was built using chained fixups, so patch tables must be used for overrides
	padding: int 					# TBD
	sharedRegionStart: int 			# base load address of cache if not slid
	sharedRegionSize: int 			# overall size required to map the cache and all subCaches, if any
	maxSlide: int 					# runtime slide of cache can be between zero and this value
	dylibsImageArrayAddr: int 		# (unslid) address of ImageArray for dylibs in this cache
	dylibsImageArraySize: int 		# size of ImageArray for dylibs in this cache
	dylibsTrieAddr: int 			# (unslid) address of trie of indexes of all cached dylibs
	dylibsTrieSize: int 			# size of trie of cached dylib paths
	otherImageArrayAddr: int 		# (unslid) address of ImageArray for dylibs and bundles with dlopen closures
	otherImageArraySize: int 		# size of ImageArray for dylibs and bundles with dlopen closures
	otherTrieAddr: int 				# (unslid) address of trie of indexes of all dylibs and bundles with dlopen closures
	otherTrieSize: int 				# size of trie of dylibs and bundles with dlopen closures
	mappingWithSlideOffset: int 	# file offset to first dyld_cache_mapping_and_slide_info
	mappingWithSlideCount: int 		# number of dyld_cache_mapping_and_slide_info entries
	dylibsPBLStateArrayAddrUnused: int  # unused
	dylibsPBLSetAddr: int 			# (unslid) address of PrebuiltLoaderSet of all cached dylibs
	programsPBLSetPoolAddr: int 	# (unslid) address of pool of PrebuiltLoaderSet for each program 
	programsPBLSetPoolSize: int 	# size of pool of PrebuiltLoaderSet for each program
	programTrieAddr: int 			# (unslid) address of trie mapping program path to PrebuiltLoaderSet
	programTrieSize: int
	osVersion: int 					# OS Version of dylibs in this cache for the main platform
	altPlatform: int 				# e.g. iOSMac on macOS
	altOsVersion: int 				# e.g. 14.0 for iOSMac
	swiftOptsOffset: int 			# VM offset from cache_header* to Swift optimizations header
	swiftOptsSize: int 				# size of Swift optimizations header
	subCacheArrayOffset: int 		# file offset to first dyld_subcache_entry
	subCacheArrayCount: int 		# number of subCache entries
	symbolFileUUID: bytes 			# unique value for the shared cache file containing unmapped local symbols
	rosettaReadOnlyAddr: int 		# (unslid) address of the start of where Rosetta can add read-only/executable data
	rosettaReadOnlySize: int 		# maximum size of the Rosetta read-only/executable region
	rosettaReadWriteAddr: int 		# (unslid) address of the start of where Rosetta can add read-write data
	rosettaReadWriteSize: int 		# maximum size of the Rosetta read-write region
	imagesOffset: int 				# file offset to first dyld_cache_image_info
	imagesCount: int 				# number of dyld_cache_image_info entries
	cacheSubType: int 				# 0 for development, 1 for production, when cacheType is multi-cache(2)
	objcOptsOffset: int 			# VM offset from cache_header* to ObjC optimizations header
	objcOptsSize: int 				# size of ObjC optimizations header
	cacheAtlasOffset: int 			# VM offset from cache_header* to embedded cache atlas for process introspection
	cacheAtlasSize: int 			# size of embedded cache atlas
	dynamicDataOffset: int 			# VM offset from cache_header* to the location of dyld_cache_dynamic_data_header
	dynamicDataMaxSize: int 		# maximum size of space reserved from dynamic data

	_fields_ = [
		("magic", c_char * 16),
		("mappingOffset", c_uint32),
		("mappingCount", c_uint32),
		("imagesOffsetOld", c_uint32),
		("imagesCountOld", c_uint32),
		("dyldBaseAddress", c_uint64),
		("codeSignatureOffset", c_uint64),
		("codeSignatureSize", c_uint64),
		("slideInfoOffsetUnused", c_uint64),
		("slideInfoSizeUnused", c_uint64),
		("localSymbolsOffset", c_uint64),
		("localSymbolsSize", c_uint64),
		("uuid", c_uint8 * 16),
		("cacheType", c_uint64),
		("branchPoolsOffset", c_uint32),
		("branchPoolsCount", c_uint32),
		("dyldInCacheMH", c_uint64),
		("dyldInCacheEntry", c_uint64),
		("imagesTextOffset", c_uint64),
		("imagesTextCount", c_uint64),
		("patchInfoAddr", c_uint64),
		("patchInfoSize", c_uint64),
		("otherImageGroupAddrUnused", c_uint64),
		("otherImageGroupSizeUnused", c_uint64),
		("progClosuresAddr", c_uint64),
		("progClosuresSize", c_uint64),
		("progClosuresTrieAddr", c_uint64),
		("progClosuresTrieSize", c_uint64),
		("platform", c_uint32),
		("formatVersion", c_uint32, 8),
		("dylibsExpectedOnDisk", c_uint32, 1),
		("simulator", c_uint32, 1),
		("locallyBuiltCache", c_uint32, 1),
		("builtFromChainedFixups", c_uint32, 1),
		("padding", c_uint32, 20),
		("sharedRegionStart", c_uint64),
		("sharedRegionSize", c_uint64),
		("maxSlide", c_uint64),
		("dylibsImageArrayAddr", c_uint64),
		("dylibsImageArraySize", c_uint64),
		("dylibsTrieAddr", c_uint64),
		("dylibsTrieSize", c_uint64),
		("otherImageArrayAddr", c_uint64),
		("otherImageArraySize", c_uint64),
		("otherTrieAddr", c_uint64),
		("otherTrieSize", c_uint64),
		("mappingWithSlideOffset", c_uint32),
		("mappingWithSlideCount", c_uint32),
		("dylibsPBLStateArrayAddrUnused", c_uint64),
		("dylibsPBLSetAddr", c_uint64),
		("programsPBLSetPoolAddr", c_uint64),
		("programsPBLSetPoolSize", c_uint64),
		("programTrieAddr", c_uint64),
		("programTrieSize", c_uint32),
		("osVersion", c_uint32),
		("altPlatform", c_uint32),
		("altOsVersion", c_uint32),
		("swiftOptsOffset", c_uint64),
		("swiftOptsSize", c_uint64),
		("subCacheArrayOffset", c_uint32),
		("subCacheArrayCount", c_uint32),
		("symbolFileUUID", c_uint8 * 16),
		("rosettaReadOnlyAddr", c_uint64),
		("rosettaReadOnlySize", c_uint64),
		("rosettaReadWriteAddr", c_uint64),
		("rosettaReadWriteSize", c_uint64),
		("imagesOffset", c_uint32),
		("imagesCount", c_uint32),
		("cacheSubType", c_uint32),
		("objcOptsOffset", c_uint64),
		("objcOptsSize", c_uint64),
		("cacheAtlasOffset", c_uint64),
		("cacheAtlasSize", c_uint64),
		("dynamicDataOffset", c_uint64),
		("dynamicDataMaxSize", c_uint64),
	]


class dyld_cache_mapping_info(Structure):
	SIZE = 32

	address: int
	size: int
	fileOffset: int
	maxProt: int
	initProt: int

	_fields_ = [
		("address", c_uint64),
		("size", c_uint64),
		("fileOffset", c_uint64),
		("maxProt", c_uint32),
		("initProt", c_uint32),
	]


class dyld_cache_mapping_and_slide_info(Structure):

	SIZE = 56

	address: int
	size: int
	fileOffset: int
	slideInfoFileOffset: int
	slideInfoFileSize: int
	flags: int
	maxProt: int
	initProt: int

	_fields_ = [
		("address", c_uint64),
		("size", c_uint64),
		("fileOffset", c_uint64),
		("slideInfoFileOffset", c_uint64),
		("slideInfoFileSize", c_uint64),
		("flags", c_uint64),
		("maxProt", c_uint32),
		("initProt", c_uint32),
	]


class dyld_cache_image_info(Structure):
	SIZE = 32

	address: int
	modTime: int
	inode: int
	pathFileOffset: int
	pad: int

	_fields_ = [
		("address", c_uint64),
		("modTime", c_uint64),
		("inode", c_uint64),
		("pathFileOffset", c_uint32),
		("pad", c_uint32),
	]


class dyld_cache_slide_info2(Structure):

	version: int 				# currently 2
	page_size: int 				# currently 4096 (may also be 16384)
	page_starts_offset: int
	page_starts_count: int
	page_extras_offset: int
	page_extras_count: int
	delta_mask: int 			# which (contiguous) set of bits contains the delta to the next rebase location
	value_add: int
	# uint16_t    page_starts[page_starts_count];
	# uint16_t    page_extras[page_extras_count];

	_fields_ = [
		("version", c_uint32),
		("page_size", c_uint32),
		("page_starts_offset", c_uint32),
		("page_starts_count", c_uint32),
		("page_extras_offset", c_uint32),
		("page_extras_count", c_uint32),
		("delta_mask", c_uint64),
		("value_add", c_uint64),
	]


class dyld_cache_slide_info3(Structure):

	version: int 			# currently 3
	page_size: int 			# currently 4096 (may also be 16384)
	page_starts_count: int
	auth_value_add: int
	# uint16_t    page_starts[/* page_starts_count */]

	_fields_ = [
		("version", c_uint32),
		("page_size", c_uint32),
		("page_starts_count", c_uint32),
		("auth_value_add", c_uint64),
	]

class dyld_cache_slide_info5(Structure):

	version: int 			# currently 5
	page_size: int 			# currently 4096 (may also be 16384)
	page_starts_count: int
	value_add: int
	# uint16_t    page_starts[/* page_starts_count */]

	_fields_ = [
		("version", c_uint32),
		("page_size", c_uint32),
		("page_starts_count", c_uint32),
		("value_add", c_uint64),
	]

if sys.byteorder == "little":
	
	class dyld_cache_slide_pointer3(Union):
		class _plain(Structure):
			pointerValue: int
			offsetToNextPointer: int
			unused: int

			_fields_ = [
				("pointerValue", c_uint64, 51),
				("offsetToNextPointer", c_uint64, 11),
				("unused", c_uint64, 2),
			]

		class _auth(Structure):
			offsetFromSharedCacheBase: int
			diversityData: int
			hasAddressDiversity: int
			key: int
			offsetToNextPointer: int
			unused: int
			authenticated: int  # = 1;

			_fields_ = [
				("offsetFromSharedCacheBase", c_uint64, 32),
				("diversityData", c_uint64, 16),
				("hasAddressDiversity", c_uint64, 1),
				("key", c_uint64, 2),
				("offsetToNextPointer", c_uint64, 11),
				("unused", c_uint64, 1),
				("authenticated", c_uint64, 1),
			]
	
		_fileOff_: int

		raw: int
		plain: _plain
		auth: _auth

		_fields_ = [
			("raw", c_uint64),
			("plain", _plain),
			("auth", _auth),
		]

		def __new__(cls, dataSource: bytes, offset=0):
			if dataSource:
				instance = None
				if memoryview(dataSource).readonly:
					instance = cls.from_buffer_copy(dataSource, offset)
				else:
					instance = cls.from_buffer(dataSource, offset)

				instance._fileOff_ = offset
				return instance
			else:
				super().__new__(cls)

		def __init__(self, dataSource: bytes, offset=0) -> None:
			pass

		def __len__(self) -> int:
			return sizeof(self)


	class dyld_cache_slide_pointer5(Union):
		class dyld_chained_ptr_arm64e_shared_cache_rebase(Structure):
			runtimeOffset: int	# offset from the start of the shared cache
			high8: int
			unused: int
			next: int 			# 8-byte slide
			auth: int 			# == 0

			_fields_ = [
				('runtimeOffset', c_uint64, 34),
				('high8', c_uint64, 8),
				('unused', c_uint64, 10),
				('next', c_uint64, 11),
				('auth', c_uint64, 1)
			]

		class dyld_chained_ptr_arm64e_shared_cache_auth_rebase(Structure):
			runtimeOffset: int	# offset from the start of the shared cache
			diversity: int
			addrDiv: int
			keyIsData: int		# implicitly always the 'A' key.  0 -> IA.  1 -> DA
			next: int			# 8-byte slide
			auth: int			# == 1

			_fields_ = [
				('runtimeOffset', c_uint64, 34),
				('diversity', c_uint64, 16),
				('addrDiv', c_uint64, 1),
				('keyIsData', c_uint64, 1),
				('next', c_uint64, 11),
				('auth', c_uint64, 1)
			]
		
		_fileOff_: int
		
		raw: int
		regular: dyld_chained_ptr_arm64e_shared_cache_rebase
		auth: dyld_chained_ptr_arm64e_shared_cache_auth_rebase
		
		_fields_ = [
			('raw', c_uint64),
			('regular', dyld_chained_ptr_arm64e_shared_cache_rebase),
			('auth', dyld_chained_ptr_arm64e_shared_cache_auth_rebase)
		]
		
		def __new__(cls, dataSource: bytes, offset=0):
			if dataSource:
				instance = None
				if memoryview(dataSource).readonly:
					instance = cls.from_buffer_copy(dataSource, offset)
				else:
					instance = cls.from_buffer(dataSource, offset)

				instance._fileOff_ = offset
				return instance
			else:
				super().__new__(cls)

		def __init__(self, dataSource: bytes, offset=0) -> None:
			pass

		def __len__(self) -> int:
			return sizeof(self)
else:
	raise NotImplementedError("Unable use a union on a big endian system!")


class dyld_cache_local_symbols_info(Structure):

	nlistOffset: int 	# offset into this chunk of nlist entries
	nlistCount: int 	# count of nlist entries
	stringsOffset: int 	# offset into this chunk of string pool
	stringsSize: int 	# byte count of string pool
	entriesOffset: int 	# offset into this chunk of array of dyld_cache_local_symbols_entry
	entriesCount: int 	# number of elements in dyld_cache_local_symbols_entry array

	_fields_ = [
		("nlistOffset", c_uint32),
		("nlistCount", c_uint32),
		("stringsOffset", c_uint32),
		("stringsSize", c_uint32),
		("entriesOffset", c_uint32),
		("entriesCount", c_uint32),
	]


class dyld_cache_local_symbols_entry(Structure):

	SIZE = 12

	dylibOffset: int 		# offset in cache file of start of dylib
	nlistStartIndex: int 	# start index of locals for this dylib
	nlistCount: int 		# number of local symbols for this dylib

	_fields_ = [
		("dylibOffset", c_uint32),
		("nlistStartIndex", c_uint32),
		("nlistCount", c_uint32),
	]


class dyld_cache_local_symbols_entry64(Structure):

	SIZE = 16

	dylibOffset: int 		# offset in cache file of start of dylib
	nlistStartIndex: int 	# start index of locals for this dylib
	nlistCount: int 		# number of local symbols for this dylib

	_fields_ = [
		("dylibOffset", c_uint64),
		("nlistStartIndex", c_uint32),
		("nlistCount", c_uint32),
	]


class dyld_subcache_entry(Structure):
	SIZE = 24

	uuid: bytes 		# The UUID of the subCache file
	cacheVMOffset: int 	# The offset of this subcache from the main cache base address

	_fields_ = [
		("uuid", c_char * 16),
		("cacheVMOffset", c_uint64),
	]


class dyld_subcache_entry2(Structure):
	SIZE = 56

	uuid: bytes 			# The UUID of the subCache file
	cacheVMOffset: int 		# The offset of this subcache from the main cache base address
	fileExtension: bytes 	# File extension of the subcache

	_fields_ = [
		("uuid", c_char * 16),
		("cacheVMOffset", c_uint64),
		("fileExtension", c_char * 32),
	]


class dyld_cache_patch_info(Structure):

	patchTableArrayAddr: int  		# (unslid) address of array for dyld_cache_image_patches for each image
	patchTableArrayCount: int  		# count of patch table entries
	patchExportArrayAddr: int  		# (unslid) address of array for patch exports for each image
	patchExportArrayCount: int  	# count of patch exports entries
	patchLocationArrayAddr: int  	# (unslid) address of array for patch locations for each patch
	patchLocationArrayCount: int  	# count of patch location entries
	patchExportNamesAddr: int  		# blob of strings of export names for patches
	patchExportNamesSize: int  		# size of string blob of export names for patches

	_fields_ = [
		("patchTableArrayAddr", c_uint64),
		("patchTableArrayCount", c_uint64),
		("patchExportArrayAddr", c_uint64),
		("patchExportArrayCount", c_uint64),
		("patchLocationArrayAddr", c_uint64),
		("patchLocationArrayCount", c_uint64),
		("patchExportNamesAddr", c_uint64),
		("patchExportNamesSize", c_uint64),
	]


class dyld_cache_image_patches(Structure):

	patchExportsStartIndex: int
	patchExportsCount: int

	_fields_ = [
		("patchExportsStartIndex", c_uint32),
		("patchExportsCount", c_uint32),
	]


class dyld_cache_patchable_export(Structure):

	SIZE: int = 16

	cacheOffsetOfImpl: int
	patchLocationsStartIndex: int
	patchLocationsCount: int
	exportNameOffset: int

	_fields_ = [
		("cacheOffsetOfImpl", c_uint32),
		("patchLocationsStartIndex", c_uint32),
		("patchLocationsCount", c_uint32),
		("exportNameOffset", c_uint32),
	]


class dyld_cache_patchable_location(Structure):

	cacheOffset: int
	high7: int
	addend: int
	authenticated: int
	usesAddressDiversity: int
	key: int
	discriminator: int

	_fields_ = [
		("cacheOffset", c_uint64, 32),
		("high7", c_uint64, 7),
		("addend", c_uint64, 5),
		("authenticated", c_uint64, 1),
		("usesAddressDiversity", c_uint64, 1),
		("key", c_uint64, 2),
		("discriminator", c_uint64, 16),
	]
