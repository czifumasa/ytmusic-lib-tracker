# ImportedCollectionDto – Export Schema (ytmlt-nestjs)

## Root DTO: ImportedCollectionDto
```ts
type ImportedCollectionDto = {
  playlists: ImportedPlaylistDto[];                       // required
  releases: ImportedReleaseDto[];                         // required
  accountInfo: ImportedConnectedAccountInfoDto;           // required
  releasesInCollection: ImportedReleaseCollectionEntryDto[]; // required
  lastSynchronize: Date;                                  // required
}
```

### Validation / serialization notes
- Arrays: `playlists`, `releases`, `releasesInCollection` must be arrays; elements are nested DTOs.
- `accountInfo` is a nested DTO.
- Dates: `lastSynchronize` must be `Date` (export as ISO-8601 string).

---

## Nested DTOs

## ImportedPlaylistDto
```ts
type ImportedPlaylistDto = {
  title: string;                     // required
  description: string | null;         // optional, default null
  youtubePlaylistId: string | null;   // optional, default null
  author: string | null;              // optional, default null
  year: string | null;                // optional, default null
  items: ImportedPlaylistItemDto[];   // required
}
```

## ImportedPlaylistItemDto
```ts
type ImportedPlaylistItemDto = {
  isAvailable: boolean;               // required, default true
  orderNumber: number | null;         // optional, default null
  youtubeTrackId: string | null;      // optional, default null
  youtubeSetItemId: string | null;    // optional, default null
}
```

### Note (possible mismatch)
- Source decorators mark `orderNumber` with `@Type(() => Number)` and TS type `number | null`,
  but also `@IsString()`. Treat `orderNumber` as a number in exports.

---

## ImportedConnectedAccountInfoDto
```ts
type ImportedConnectedAccountInfoDto = {
  accountName: string;            // required, non-empty
  accountPhotoUrl: string | null; // optional; if present must be non-empty string
  url: string;                    // required
}
```

---

## ImportedReleaseDto
```ts
type ImportedReleaseDto = {
  code: string | null;                 // optional, default null
  title: string;                       // required
  releaseType: ReleaseType;             // required enum
  releaseYear: string | null;           // optional, default null
  creditedName: string | null;          // optional, default null
  url: string | null;                   // optional, default null
  youtubeBrowseId: string | null;        // optional, default null
  youtubePlaylistId: string | null;      // optional, default null
  primaryArtists: ImportedArtistDto[];   // required, default []
  tracks: ImportedReleaseTrackDto[];     // required, default []
  completeTrackList: boolean;            // required, default false
  isUserUploaded: boolean;               // required, default false
}
```

## ReleaseType (enum)
```ts
type ReleaseType =
  | "ALBUM"
  | "EP"
  | "SINGLE"
  | "UNAUTH"
  | "ADDITIONAL"
  | "COMP"
  | "OTHER"
  | "UNKNOWN";
```

---

## ImportedArtistDto
```ts
type ImportedArtistDto = {
  code: string | null;               // optional, default null
  youtubeChannelId: string | null;    // optional, default null
  fullName: string;                   // required
  localizedFullName: string | null;   // optional, default null
  url: string | null;                 // optional, default null
}
```

---

## ImportedReleaseTrackDto
```ts
type ImportedReleaseTrackDto = {
  youtubeTrackId: string | null;         // optional, default null
  title: string;                          // required
  creditedName: string | null;            // optional, default null
  trackNumber: string | null;             // optional, default null
  primaryArtists: ImportedArtistDto[];    // required, default []
  orderNumber: number | null;             // optional, default null
  isAvailable: boolean;                   // required
}
```

---

## ImportedReleaseCollectionEntryDto
```ts
type ImportedReleaseCollectionEntryDto = {
  releaseCode: string | null;              // optional, default null
  releaseYoutubeBrowseId: string | null;   // optional, default null
  isUserUploaded: boolean;                 // required, default false
  rating: number | null;                   // optional
  ratedOn: Date | null;                    // optional
  trackRatings: ImportedTrackCollectionEntryDto[]; // required
}
```

## ImportedTrackCollectionEntryDto
```ts
type ImportedTrackCollectionEntryDto = {
  orderNumber: number | null;        // optional, default null
  youtubeTrackId: string | null;     // optional, default null
  isUserUploaded: boolean;           // required, default false
  rating: number | null;             // optional
}
```

---

## Export recommendations
- Dates: export `Date` values as ISO-8601 strings:
  - `lastSynchronize`
  - `ratedOn`
- For stable shape, emit explicit `null` for nullable fields instead of omitting them.
- Ensure required arrays exist (use `[]` if empty):
  - `playlists`, `releases`, `releasesInCollection`
  - `ImportedPlaylistDto.items`
  - `ImportedReleaseDto.primaryArtists`, `ImportedReleaseDto.tracks`
  - `ImportedReleaseCollectionEntryDto.trackRatings`
